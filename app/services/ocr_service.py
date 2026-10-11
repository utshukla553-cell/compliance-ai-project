from pathlib import Path

import pytesseract
from PIL import Image


def extract_text_from_image(image_path: str) -> str:
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {image_path}")

    image = Image.open(path)
    text = pytesseract.image_to_string(image)

    return text.strip()
