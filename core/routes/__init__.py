# core/routes/__init__.py
from .login import auth_bp
from .api import api_bp  # we'll create api.py later (placeholder)

def register_routes(app):
    """
    Register all route blueprints here.
    Keep a single place to add new route modules.
    """
    app.register_blueprint(auth_bp, url_prefix="/api")
    # register other blueprints when created:
    # app.register_blueprint(api_bp, url_prefix="/api")
