# Libraries
import os
from models.ocr_document_model import OCRDocumentModel


# OCR Document Controller
class OCRDocumentController:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.UPLOAD_DIR = os.path.join(self.BASE_DIR, "uploads")

        if not os.path.exists(self.UPLOAD_DIR):
            os.makedirs(self.UPLOAD_DIR)

        self.ocr_document_model = OCRDocumentModel()

    def handle_ocr_upload(self, file):
        if file is None or not getattr(file, "filename", None):
            return "No file uploaded"
        
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in self.ocr_document_model.SUPPORTED_IMAGE:
            return "Only PNG, JPG, JPEG images are allowed"

        file_path = os.path.join(self.UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as f:
            f.write(file.file.read())

        return self.ocr_document_model.perform_ocr(file_path)