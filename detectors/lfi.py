# core/detectors/lfi.py
import re

LFI_PATTERNS = [
    re.compile(r"(\.\./|\.\.\\)"),
    re.compile(r"(?i)(/etc/passwd)"),
    re.compile(r"(?i)(boot.ini)"),
    re.compile(r"(?i)(windows/system32)"),
]

def detect_lfi(text):
    matches = []
    if not text:
        return False, matches
    for p in LFI_PATTERNS:
        if p.search(text):
            matches.append(p.pattern)
    return (len(matches) > 0), matches
