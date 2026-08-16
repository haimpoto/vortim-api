"""
שלב 4 — הרשמה והתחברות. מייצר משתמש בדיקה, מתחבר, ובודק סיסמה שגויה.
"""
from _helpers import post, is_json, check, summary

print("STAGE 4 — auth")

USER = {"username": "test_user", "password": "secret123"}

# register (if already exists the server may return 400 — that's fine for a re-run)
r = post("/register", json=USER)
check(r.status_code in (200, 201, 400), "POST /register responds (200/201, or 400 if exists)")

# login with correct password
r = post("/login", json=USER)
check(r.status_code == 200, "login with correct password -> 200")
token = None
if is_json(r):
    body = r.json()
    token = body.get("token") or body.get("access_token") or body.get("jwt")
check(bool(token), "login returns a token")

# login with wrong password
r = post("/login", json={"username": USER["username"], "password": "WRONG"})
check(r.status_code == 401, "login with wrong password -> 401")

exit(0 if summary() else 1)
