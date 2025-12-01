# app.py
import os
from core import create_app

if __name__ == "__main__":
    # read host/port from env for flexibility
    host = os.environ.get("HONEYPOT_HOST", "0.0.0.0")
    port = int(os.environ.get("HONEYPOT_PORT", 5000))
    debug = os.environ.get("HONEYPOT_DEBUG", "True").lower() in ("1", "true", "yes")

    app = create_app()
    app.run(host=host, port=port, debug=debug)
