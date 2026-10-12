from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    from app.routes.api import api

    app.register_blueprint(api, url_prefix="/api")

    @app.get("/")
    def home():
        return render_template("index.html")

    return app
