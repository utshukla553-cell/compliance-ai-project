import json
import logging
import os
import re

from dotenv import load_dotenv
from langdetect import detect

load_dotenv()

logger = logging.getLogger(__name__)


DATE_PATTERNS = [
    r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
    r"\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b",
    r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\b",
]


IMPORTANT_WORDS = [
    "must",
    "shall",
    "required",
    "mandatory",
    "deadline",
    "penalty",
    "compliance",
    "prohibited",
    "effective from",
    "valid until",
]


HIGH_PRIORITY_WORDS = [
    "penalty",
    "immediate",
    "urgent",
    "deadline",
    "legal action",
    "non-compliance",
]


MEDIUM_PRIORITY_WORDS = [
    "required",
    "mandatory",
    "compliance",
    "shall",
    "must",
]


def detect_language(text: str) -> str:
    """Detect the language of the document text."""

    if not text or not text.strip():
        return "unknown"

    try:
        return detect(text)
    except Exception as exc:
        logger.warning("Language detection failed: %s", exc)
        return "unknown"


def extract_dates(text: str) -> list[str]:
    """Find common date formats in document text."""

    if not text:
        return []

    found_dates = []

    for pattern in DATE_PATTERNS:
        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        for match in matches:
            if match not in found_dates:
                found_dates.append(match)

    return found_dates


def find_important_clauses(text: str) -> list[str]:
    """Find sentences containing compliance-related keywords."""

    if not text:
        return []

    clauses = []

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text,
    )

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        sentence_lower = sentence.lower()

        for keyword in IMPORTANT_WORDS:
            if keyword in sentence_lower:
                clauses.append(sentence)
                break

        if len(clauses) >= 10:
            break

    return clauses


def calculate_priority(text: str) -> str:
    """Calculate priority using rule-based analysis."""

    if not text:
        return "Low"

    document_text = text.lower()

    for keyword in HIGH_PRIORITY_WORDS:
        if keyword in document_text:
            return "High"

    for keyword in MEDIUM_PRIORITY_WORDS:
        if keyword in document_text:
            return "Medium"

    return "Low"


def _clean_ai_response(response_text: str) -> str:
    """Remove Markdown code fences from an AI response."""

    response_text = response_text.strip()

    if response_text.startswith("```"):
        response_text = re.sub(
            r"^```(?:json)?\s*",
            "",
            response_text,
            flags=re.IGNORECASE,
        )

        response_text = re.sub(
            r"\s*```$",
            "",
            response_text,
        )

    return response_text.strip()


def analyze_with_gemini(text: str) -> dict:
    """
    Analyze document using Gemini.

    If Gemini is unavailable or rate-limited,
    return an empty dictionary so the application
    can use the local rule-based fallback.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        logger.warning(
            "GEMINI_API_KEY is not configured. "
            "Using local document analysis."
        )
        return {}

    try:
        from google import genai

        client = genai.Client(api_key=api_key)

        prompt = f"""
Analyze the following compliance document.

Return ONLY a valid JSON object with these fields:

summary
important_clauses
compliance_dates
checklist
priority
document_type

Requirements:
- summary should be short and clear.
- important_clauses should be an array.
- compliance_dates should be an array.
- checklist should contain short actionable tasks.
- priority should be High, Medium, or Low.
- document_type should describe the document type.

Document:
{text[:12000]}
"""

        response = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt,
        )

        response_text = getattr(
            response,
            "output_text",
            "",
        )

        if not response_text:
            logger.warning(
                "Gemini returned an empty response. "
                "Using local analysis."
            )
            return {}

        response_text = _clean_ai_response(
            response_text
        )

        result = json.loads(response_text)

        if not isinstance(result, dict):
            logger.warning(
                "Gemini response was not a JSON object."
            )
            return {}

        return result

    except Exception as exc:
        error_message = str(exc).lower()

        # Gemini Free Tier rate limit
        if (
            "429" in error_message
            or "rate limit" in error_message
            or "too_many_requests" in error_message
        ):
            logger.warning(
                "Gemini API rate limit reached. "
                "Using local rule-based analysis instead."
            )
            return {}

        # Any other Gemini/API error
        logger.warning(
            "Gemini analysis unavailable: %s",
            exc,
        )

        return {}


def analyze_document(text: str) -> dict:
    """
    Analyze a document using Gemini first.

    If Gemini is unavailable, automatically use
    local rule-based analysis.
    """

    language = detect_language(text)

    # Try Gemini
    ai_result = analyze_with_gemini(text)

    # Gemini succeeded
    if ai_result:
        return {
            "language": language,
            "summary": ai_result.get(
                "summary",
                "",
            ),
            "important_clauses": ai_result.get(
                "important_clauses",
                [],
            ),
            "compliance_dates": ai_result.get(
                "compliance_dates",
                [],
            ),
            "checklist": ai_result.get(
                "checklist",
                [],
            ),
            "priority": ai_result.get(
                "priority",
                "Medium",
            ),
            "document_type": ai_result.get(
                "document_type",
                "Other",
            ),
        }

    # Gemini unavailable → local fallback
    logger.info(
        "Gemini unavailable. "
        "Using rule-based document analysis."
    )

    return {
        "language": language,
        "summary": text[:500].strip(),
        "important_clauses": find_important_clauses(text),
        "compliance_dates": extract_dates(text),
        "checklist": [],
        "priority": calculate_priority(text),
        "document_type": "Other",
    }