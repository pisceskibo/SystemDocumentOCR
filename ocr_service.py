import pytesseract
from PIL import Image
from pdf2image import convert_from_path

def run_ocr(file_path):
    text = ""

    if file_path.lower().endswith(".pdf"):
        images = convert_from_path(file_path)
        for img in images:
            text += pytesseract.image_to_string(img)
    else:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)

    return text
