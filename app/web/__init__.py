from flask import Flask

from app.config import settings


def create_flask_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )
    app.config["SECRET_KEY"] = settings.SECRET_KEY

    from app.web.routes import web_bp
    app.register_blueprint(web_bp)

    return app