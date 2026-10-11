from pathlib import Path

import fitz
import pdfplumber


def extract_text_from_pdf(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    text_parts = []

    with fitz.open(path) as pdf:
        for page in pdf:
            text = page.get_text("text")
            if text:
                text_parts.append(text)

    text = "\n".join(text_parts).strip()

    if text:
        return text

    # Fallback for PDFs where PyMuPDF cannot extract useful text.
    fallback_parts = []

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                fallback_parts.append(page_text)

    return "\n".join(fallback_parts).strip()
