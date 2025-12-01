# core/detectors/brute_force.py
import time
from collections import defaultdict, deque

# in-memory store for attempts: { ip: deque([timestamp, ...]) }
_ATTEMPT_WINDOW = defaultdict(lambda: deque(maxlen=200))
WINDOW_SECONDS = 60  # sliding window length
THRESHOLD = 10       # attempts within WINDOW_SECONDS considered brute-force

def register_attempt(ip):
    now = time.time()
    dq = _ATTEMPT_WINDOW[ip]
    dq.append(now)
    # remove old entries
    while dq and dq[0] < now - WINDOW_SECONDS:
        dq.popleft()
    return len(dq)

def is_bruteforce(ip):
    count = register_attempt(ip)
    return count >= THRESHOLD, count
