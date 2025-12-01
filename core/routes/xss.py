# core/routes/xss.py
from flask import Blueprint, request, jsonify
from datetime import datetime
from ..utils.logger import log_attack

xss_bp = Blueprint("xss", __name__)

@xss_bp.route("/comment", methods=["GET", "POST"])
def comment():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ua = request.headers.get("User-Agent", "")
    if request.method == "POST":
        if request.is_json:
            payload = request.get_json()
        else:
            payload = request.form.to_dict() or {"raw": request.get_data(as_text=True)}
    else:
        payload = request.args.to_dict()

    doc = {
        "endpoint": "/comment",
        "method": request.method,
        "remote_ip": ip,
        "user_agent": ua,
        "raw_payload": payload,
        "timestamp": datetime.utcnow().isoformat()
    }

    log_attack(doc)
    # Simulate storing comment (do not render back user input unsafely)
    return jsonify({"status": "ok", "message": "Comment received"}), 200
