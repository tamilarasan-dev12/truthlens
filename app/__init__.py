from pathlib import Path

from flask import Flask, jsonify, request

from config import Config
from database.db import init_app as init_db


def create_app(config_class=Config):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(config_class)

    app.config["DATABASE"] = str(app.config["DATABASE"])
    app.config["MODEL_PATH"] = str(app.config["MODEL_PATH"])
    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)

    init_db(app)

    from app.routes import bp as main_bp

    app.register_blueprint(main_bp)

    @app.errorhandler(400)
    def bad_request(_error):
        if request.path.startswith("/api/"):
            return (
                jsonify({"status": "error", "data": None, "error": "Bad request"}),
                400,
            )
        return "Bad request", 400

    @app.errorhandler(500)
    def server_error(_error):
        if request.path.startswith("/api/"):
            return (
                jsonify(
                    {"status": "error", "data": None, "error": "Internal server error"}
                ),
                500,
            )
        return "Internal server error", 500

    return app
