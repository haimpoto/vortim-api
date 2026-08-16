"""
שלב 3 — הפרשה הנוכחית.
"""
from _helpers import get, is_json, check, summary

print("STAGE 3 — current parsha")

r = get("/current")
check(r.status_code == 200, "GET /current -> 200")
check(is_json(r), "returns JSON with the current parsha name")

r = get("/current/vortim")
check(r.status_code == 200, "GET /current/vortim -> 200")
check(is_json(r), "current parsha vortim returns JSON")

exit(0 if summary() else 1)
