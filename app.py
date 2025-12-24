from pyramid.config import Configurator
from pyramid.view import view_config
from waitress import serve
from pdf2image import convert_from_path
import os
from PIL import Image
import pytesseract

import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


@view_config(route_name="home", renderer="index.html", request_method="GET")
def home_view(request):
    return {"ocr_text": ""}


@view_config(route_name="ocr", renderer="index.html", request_method="POST")
def ocr_view(request):
    file = request.POST.get("file")
    text = ""

    if file is None or not getattr(file, "filename", None):
        return {"ocr_text": "No file uploaded"}

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    ext = os.path.splitext(file.filename)[1].lower()

    try:
        if ext in [".png", ".jpg", ".jpeg"]:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image, lang="eng")

        elif ext == ".pdf":
            from pdf2image import convert_from_path
            pages = convert_from_path(file_path, dpi=300)
            for i, page in enumerate(pages):
                text += f"\n--- Page {i+1} ---\n"
                text += pytesseract.image_to_string(page, lang="eng")

        else:
            text = "Unsupported file format"

    except Exception as e:
        text = f"OCR error: {str(e)}"

    return {"ocr_text": text}


if __name__ == "__main__":
    with Configurator(
        settings={
            "pyramid.debug_all": True,
            "jinja2.directories": "templates"
        }
    ) as config:
        config.include("pyramid_jinja2")
        config.add_renderer(".html", "pyramid_jinja2.renderer_factory")


        config.add_static_view(name="static", path=os.path.join(BASE_DIR, "static"))

        config.add_route("home", "/")
        config.add_route("ocr", "/ocr")

        config.scan()

        app = config.make_wsgi_app()

    print(">>> OCR Pyramid Server running at http://127.0.0.1:8000")
    serve(app, host="127.0.0.1", port=8000)
