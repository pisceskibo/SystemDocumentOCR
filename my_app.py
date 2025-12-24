# Libraries
import os
from pyramid.config import Configurator
from waitress import serve

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    with Configurator(
        settings={
            "pyramid.debug_all": True,
            "jinja2.directories": os.path.join(BASE_DIR, "templates")
        }
    ) as config:

        config.include("pyramid_jinja2")
        config.add_renderer(".html", "pyramid_jinja2.renderer_factory")

        config.add_static_view(
            name="static", path=os.path.join(BASE_DIR, "static")
        )

        config.add_route("home", "/")
        config.add_route("ocr", "/ocr")

        config.scan("views")

        app = config.make_wsgi_app()

    print(">>> OCR Pyramid Server running at http://127.0.0.1:8000")
    serve(app, host="127.0.0.1", port=8000)