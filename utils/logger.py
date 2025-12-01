# core/utils/logger.py
import os
import json
from datetime import datetime
from flask import current_app
from ..database.mongo import get_db

LOG_DIR = os.path.join(os.getcwd(), "data", "raw_logs")
os.makedirs(LOG_DIR, exist_ok=True)

def _write_local_file(doc):
    """Write a single JSON line to local raw_logs for backup."""
    fname = os.path.join(LOG_DIR, f"{datetime.utcnow().date().isoformat()}.log")
    with open(fname, "a", encoding="utf-8") as f:
        f.write(json.dumps(doc, default=str) + "\n")

def log_attack(doc):
    """
    Insert attack document into MongoDB and append to local file.
    doc: a dict with attack info
    """
    try:
        db = get_db()
        coll = db["attacks"]
        coll.insert_one(doc)
    except Exception as e:
        # if Mongo is down, still persist locally
        try:
            current_app.logger.warning(f"Mongo insert failed: {e}. Writing to local file.")
        except RuntimeError:
            # current_app not available (e.g., called outside request/context)
            pass
    finally:
        # Always write a local backup
        try:
            _write_local_file(doc)
        except Exception:
            pass
