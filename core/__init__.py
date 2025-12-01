# core/__init__.py
import os
from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__, static_folder="../frontend/dist", template_folder="templates")

    # Basic config
    app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb://localhost:27017/intelligent_honeypot")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-secret")

    # Enable CORS so React frontend (dev server) can call backend during development
    CORS(app)

    # initialize db
    from .database.mongo import init_db
    init_db(app)

    # register route blueprints
    from .routes import register_routes
    register_routes(app)

    # basic health check
    @app.route("/health")
    def health():
        return {"status": "ok", "service": "intelligent-honeypot-backend"}

    return app
