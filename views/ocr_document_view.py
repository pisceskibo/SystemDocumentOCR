# Libraries
from pyramid.view import view_config
from controllers.ocr_document_controller import OCRDocumentController


class OCRDocumentView:
    def __init__(self, request):
        self.request = request
        self.ocr_document_controller = OCRDocumentController()

    @view_config(route_name="home", renderer="index.html", request_method="GET")
    def home_view(self):
        return {"ocr_text": ""}

    @view_config(route_name="ocr", renderer="index.html", request_method="POST")
    def ocr_view(self):
        file = self.request.POST.get("file")
        text = self.ocr_document_controller.handle_ocr_upload(file)
        return {"ocr_text": text}