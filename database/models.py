# core/database/models.py
"""
Lightweight helpers for document shapes. Not strict schema enforcement (MongoDB).
"""

def build_attack_doc(base):
    """
    Ensure minimal fields are present and normalized.
    base: dict collected in routes
    """
    doc = {}
    doc.update(base)
    # ensure timestamp is ISO string
    if "timestamp" not in doc:
        from datetime import datetime
        doc["timestamp"] = datetime.utcnow().isoformat()
    # normalize attack_type as list
    if "attack_type" not in doc:
        doc["attack_type"] = []
    return doc
