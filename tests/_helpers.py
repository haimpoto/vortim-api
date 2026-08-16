"""
פונקציות עזר לטסטים. אתה לא צריך לגעת בקובץ הזה.
"""
import requests
from config import BASE_URL

_passed = 0
_failed = 0

def check(condition, description):
    global _passed, _failed
    if condition:
        _passed += 1
        print("  [PASS]", description)
    else:
        _failed += 1
        print("  [FAIL]", description)

def get(path, token=None, **kwargs):
    headers = kwargs.pop("headers", {})
    if token:
        headers["Authorization"] = "Bearer " + token
    return requests.get(BASE_URL + path, headers=headers, timeout=5, **kwargs)

def post(path, token=None, **kwargs):
    headers = kwargs.pop("headers", {})
    if token:
        headers["Authorization"] = "Bearer " + token
    return requests.post(BASE_URL + path, headers=headers, timeout=5, **kwargs)

def is_json(resp):
    try:
        resp.json()
        return True
    except Exception:
        return False

def summary():
    print()
    print("=" * 40)
    print(f"  PASS: {_passed}    FAIL: {_failed}")
    print("=" * 40)
    return _failed == 0
