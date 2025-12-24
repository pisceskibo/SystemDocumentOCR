# Libraries
import os
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# OCR Document Model
class OCRDocumentModel:
    def __init__(self):
        self.SUPPORTED_IMAGE = [".png", ".jpg", ".jpeg"]
        self.SUPPORTED_PDF = [".pdf"]

    def perform_ocr(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        text = ""

        if ext in self.SUPPORTED_IMAGE:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image, lang="eng")

        elif ext in self.SUPPORTED_PDF:
            pages = convert_from_path(file_path, dpi=300)
            for i, page in enumerate(pages):
                text += f"\n--- Page {i+1} ---\n"
                text += pytesseract.image_to_string(page, lang="eng")
                
        else:
            text = "Unsupported file format"

        return text