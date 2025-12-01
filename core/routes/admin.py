# core/routes/admin.py
from flask import Blueprint, request, jsonify
from datetime import datetime
from ..utils.logger import log_attack
from ..utils.geoip import lookup_ip

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ua = request.headers.get("User-Agent", "")
    payload = {}
    if request.method == "POST":
        if request.is_json:
            payload = request.get_json()
        else:
            payload = request.form.to_dict() or request.get_data(as_text=True)
    else:
        payload = request.args.to_dict()

    doc = {
        "endpoint": "/admin/login",
        "method": request.method,
        "remote_ip": ip,
        "user_agent": ua,
        "raw_payload": payload,
        "timestamp": datetime.utcnow().isoformat()
    }

    # enrich with geo if available
    try:
        geo = lookup_ip(ip)
        if geo:
            doc["geo"] = geo
    except Exception:
        pass

    log_attack(doc)
    # Return a plausible admin page (but as API we return JSON)
    return jsonify({"status": "error", "message": "Access denied"}), 403

@admin_bp.route("/admin/panel", methods=["GET"])
def admin_panel():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    doc = {
        "endpoint": "/admin/panel",
        "method": "GET",
        "remote_ip": ip,
        "user_agent": request.headers.get("User-Agent", ""),
        "raw_payload": {},
        "timestamp": datetime.utcnow().isoformat()
    }
    log_attack(doc)
    # Return some fake HTML to appear real if visited by browser
    html = "<html><body><h1>Admin Panel</h1><p>Unauthorized</p></body></html>"
    return html, 401
