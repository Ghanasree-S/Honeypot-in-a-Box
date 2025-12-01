# core/routes/login.py
from flask import Blueprint, request, jsonify
from datetime import datetime
from ..utils.logger import log_attack

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def fake_login():
    """
    A fake login endpoint that logs every attempt.
    Always returns invalid credentials (so attackers keep trying).
    """
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ua = request.headers.get("User-Agent", "")
    payload = {}

    if request.method == "POST":
        # Accept both form and JSON payloads
        if request.is_json:
            payload = request.get_json()
            username = payload.get("username")
            password = payload.get("password")
        else:
            payload = request.form.to_dict() or request.get_data(as_text=True)
            username = request.form.get("username")
            password = request.form.get("password")
    else:
        # GET requests — attackers sometimes probe via GET
        username = request.args.get("username")
        password = request.args.get("password")
        payload = request.args.to_dict()

    doc = {
        "endpoint": "/api/login",
        "method": request.method,
        "remote_ip": ip,
        "user_agent": ua,
        "username": username,
        "password": password,
        "raw_payload": payload,
        "timestamp": datetime.utcnow().isoformat()
    }

    # Log into DB (and file)
    log_attack(doc)

    # Return plausible response (always unsuccessful)
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401
