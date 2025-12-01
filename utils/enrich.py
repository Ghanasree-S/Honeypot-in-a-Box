# core/utils/enrich.py  (new file)
from .logger import log_attack as _base_log_attack
from ..detectors.sql_injection import detect_sql_injection
from ..detectors.xss import detect_xss
from ..detectors.lfi import detect_lfi
from ..detectors.brute_force import is_bruteforce

def enrich_and_log(doc):
    """
    Run detectors, add fields attack_type and attack_score, then call base logger.
    """
    text_candidates = []
    # collect text blobs to scan
    raw = doc.get("raw_payload") or ""
    if isinstance(raw, dict):
        # join values
        for v in raw.values():
            text_candidates.append(str(v))
    else:
        text_candidates.append(str(raw))

    # join into a single string for basic detection
    text = " ".join(text_candidates)

    attack_types = []
    score = 0.0

    sqli, sqli_matches = detect_sql_injection(text)
    if sqli:
        attack_types.append("sql_injection")
        score += 0.5

    xss, xss_matches = detect_xss(text)
    if xss:
        attack_types.append("xss")
        score += 0.5

    lfi, lfi_matches = detect_lfi(text)
    if lfi:
        attack_types.append("lfi")
        score += 0.4

    # brute force detection from remote_ip if present
    ip = doc.get("remote_ip")
    if ip:
        bf, count = is_bruteforce(ip)
        if bf:
            attack_types.append("brute_force")
            # scale score by attempts
            score += min(1.0, count / 20.0)

    doc["attack_type"] = attack_types
    doc["attack_score"] = round(min(score, 1.0), 2)
    # add matches if wanted
    doc["detector_matches"] = {
        "sqli": sqli_matches if sqli else [],
        "xss": xss_matches if xss else [],
        "lfi": lfi_matches if lfi else []
    }

    # Call base logger (writes to mongo + file)
    _base_log_attack(doc)
