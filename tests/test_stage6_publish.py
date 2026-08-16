"""
שלב 6 — פרסום ובדיקות תוכן. admin מפרסם וורט תקין (201), תוכן פגום נדחה (400),
משתמש רגיל נחסם (403).
"""
from _helpers import get, post, is_json, check, summary

print("STAGE 6 — publish + validation")

# 'admin' is listed in data/admins.json — register + login it
ADMIN = {"username": "admin", "password": "adminpass"}
post("/register", json=ADMIN)
r = post("/login", json=ADMIN)
admin_token = None
if is_json(r):
    b = r.json()
    admin_token = b.get("token") or b.get("access_token") or b.get("jwt")
check(bool(admin_token), "admin can log in")

good_vort = {
    "id": "vort_test_ok",
    "title": "וורט בדיקה",
    "author": "בודק",
    "text": "טקסט תקין באורך מספיק לצורך הבדיקה של המערכת.",
}
if admin_token:
    r = post("/parshiot/bereshit/vortim", token=admin_token, json=good_vort)
    check(r.status_code == 201, "admin publishes a valid vort -> 201")

    bad_vort = {"title": "x", "author": "בודק", "text": "קצר"}  # title too short, missing id, text too short
    r = post("/parshiot/bereshit/vortim", token=admin_token, json=bad_vort)
    check(r.status_code == 400, "invalid content -> 400")
else:
    check(False, "no admin token — skipping publish checks")

# a regular (non-admin) user must be blocked
REG = {"username": "test_user", "password": "secret123"}
post("/register", json=REG)
r = post("/login", json=REG)
reg_token = None
if is_json(r):
    b = r.json()
    reg_token = b.get("token") or b.get("access_token") or b.get("jwt")
if reg_token:
    r = post("/parshiot/bereshit/vortim", token=reg_token, json=good_vort)
    check(r.status_code == 403, "non-admin publishing -> 403")
else:
    check(False, "no regular-user token")

exit(0 if summary() else 1)
