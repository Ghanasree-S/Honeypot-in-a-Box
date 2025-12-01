# core/database/mongo.py
from pymongo import MongoClient
from flask import current_app, g

def init_db(app):
    """
    Initialize MongoDB client and attach to app context.
    """
    uri = app.config.get("MONGO_URI")
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    # Optionally test connection
    try:
        client.server_info()
    except Exception as e:
        app.logger.warning(f"Could not connect to MongoDB: {e}")

    # store client in app.extensions
    app.extensions = getattr(app, "extensions", {})
    app.extensions["mongo_client"] = client

def get_db():
    """
    Return a MongoDB database object for the configured URI.
    """
    client = current_app.extensions.get("mongo_client")
    if client is None:
        raise RuntimeError("Mongo client not initialized. Call init_db(app) first.")
    # DB name is last path in URI or default
    db_name = current_app.config.get("MONGO_URI").rsplit("/", 1)[-1] or "intelligent_honeypot"
    return client[db_name]
