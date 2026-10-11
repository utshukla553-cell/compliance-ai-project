from pathlib import Path

from app.services.ai_service import analyze_document
from app.services.document_service import extract_text_from_pdf
from app.services.ocr_service import extract_text_from_image


def process_document(file_path: str) -> dict:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    extension = path.suffix.lower()

    if extension == ".pdf":
        text = extract_text_from_pdf(file_path)

    elif extension in [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
        text = extract_text_from_image(file_path)

    else:
        raise ValueError(
            "Unsupported file type. Please upload a PDF or image file."
        )

    if not text.strip():
        raise ValueError(
            "No readable text was found in the document."
        )

    analysis = analyze_document(text)

    return {
        "filename": path.name,
        "file_path": str(path),
        "text": text,
        **analysis,
    }
