# core/detectors/sql_injection.py
import re

SQLI_PATTERNS = [
    re.compile(r"(?i)(\bUNION\b.*\bSELECT\b)"),
    re.compile(r"(?i)(\bSELECT\b.+\bFROM\b)"),
    re.compile(r"(?i)(\bOR\b\s+\d+\s*=\s*\d+)"),
    re.compile(r"(?i)(\bAND\b\s+\d+\s*=\s*\d+)"),
    re.compile(r"(?i)(\b--\b|\#\b|;--|;|\b/\*.*\*/\b)"),
    re.compile(r"(?i)['\"`].*=\s*['\"`]")
]

def detect_sql_injection(text):
    """
    Returns (matched, matches_list)
    """
    matches = []
    if not text:
        return False, matches
    for p in SQLI_PATTERNS:
        if p.search(text):
            matches.append(p.pattern)
    return (len(matches) > 0), matches
