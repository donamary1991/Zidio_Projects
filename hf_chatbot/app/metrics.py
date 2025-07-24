# app/metrics.py
import time

def track_metrics(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        return result, duration
    return wrapper
