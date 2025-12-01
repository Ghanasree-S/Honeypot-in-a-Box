# core/routes/api.py
from flask import Blueprint, request, jsonify, current_app
from ..database.mongo import get_db
from datetime import datetime, timedelta

api_bp = Blueprint("api", __name__)

@api_bp.route("/attacks", methods=["GET"])
def get_attacks():
    """
    Query params:
      - limit (int)
      - since (ISO datetime)
      - ip, type, endpoint
    """
    db = get_db()
    coll = db["attacks"]

    q = {}
    limit = int(request.args.get("limit", 100))
    since = request.args.get("since")
    if since:
        try:
            since_dt = datetime.fromisoformat(since)
            q["timestamp"] = {"$gte": since_dt.isoformat()}
        except Exception:
            pass

    ip = request.args.get("ip")
    if ip:
        q["remote_ip"] = ip

    attack_type = request.args.get("type")
    if attack_type:
        q["attack_type"] = attack_type

    endpoint = request.args.get("endpoint")
    if endpoint:
        q["endpoint"] = endpoint

    docs = list(coll.find(q).sort("timestamp", -1).limit(limit))
    # convert ObjectId to str and ensure JSON serializable
    for d in docs:
        d["_id"] = str(d.get("_id"))
    return jsonify({"count": len(docs), "results": docs})

@api_bp.route("/stats/summary", methods=["GET"])
def stats_summary():
    db = get_db()
    coll = db["attacks"]
    now = datetime.utcnow()
    last_24 = now - timedelta(hours=24)
    total = coll.count_documents({})
    last24 = coll.count_documents({"timestamp": {"$gte": last_24.isoformat()}})
    # top IPs
    pipeline = [
        {"$group": {"_id": "$remote_ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_ips = list(coll.aggregate(pipeline))
    # attack type distribution
    pipeline2 = [
        {"$unwind": {"path": "$attack_type", "preserveNullAndEmptyArrays": True}},
        {"$group": {"_id": "$attack_type", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    types = list(coll.aggregate(pipeline2))
    return jsonify({
        "total_attacks": total,
        "attacks_last_24h": last24,
        "top_ips": top_ips,
        "attack_types": types
    })
