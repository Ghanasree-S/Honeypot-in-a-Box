# core/detectors/xss.py
import re

XSS_PATTERNS = [
    re.compile(r"(?i)<\s*script\b"),
    re.compile(r"(?i)onerror\s*="),
    re.compile(r"(?i)onload\s*="),
    re.compile(r"(?i)<\s*iframe\b"),
    re.compile(r"(?i)<\s*img\b"),
    re.compile(r"(?i)javascript:\s*"),
]

def detect_xss(text):
    matches = []
    if not text:
        return False, matches
    for p in XSS_PATTERNS:
        if p.search(text):
            matches.append(p.pattern)
    return (len(matches) > 0), matches
