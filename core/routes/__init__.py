# core/routes/__init__.py
from .login import auth_bp
from .api import api_bp
from .admin import admin_bp
from .xss import xss_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/api")
    app.register_blueprint(xss_bp, url_prefix="/api")
