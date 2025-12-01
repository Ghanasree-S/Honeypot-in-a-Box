# core/utils/alerts.py
import logging
import os

ALERT_LOG = os.path.join(os.getcwd(), "data", "alerts.log")
logging.basicConfig(filename=ALERT_LOG, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def alert(info):
    """
    info: dict or string describing the alert
    Current implementation logs to alerts.log and prints.
    """
    msg = info if isinstance(info, str) else str(info)
    logging.info(msg)
    print("[ALERT]", msg)
