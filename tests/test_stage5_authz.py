"""
שלב 5 — הרשאות. וורט ארוך בודד: אורח מקבל 403, משתמש מחובר מקבל 200.
ההחלטה על התנהגות הרשימה השלמה לאורח היא שלך — הטסט לא בודק אותה.
"""
from _helpers import get, post, is_json, check, summary

print("STAGE 5 — authorization")

USER = {"username": "test_user", "password": "secret123"}
post("/register", json=USER)  # ensure exists
r = post("/login", json=USER)
token = None
if is_json(r):
    b = r.json()
    token = b.get("token") or b.get("access_token") or b.get("jwt")

# a known LONG vort from the sample data: bereshit/vort_03
r = get("/parshiot/bereshit/vortim/vort_03")           # as guest
check(r.status_code == 403, "guest requesting a LONG vort -> 403")

if token:
    r = get("/parshiot/bereshit/vortim/vort_03", token=token)  # logged in
    check(r.status_code == 200, "logged-in user gets the LONG vort -> 200")
else:
    check(False, "could not obtain token (check stage 4 first)")

# a SHORT vort is open to everyone
r = get("/parshiot/bereshit/vortim/vort_01")
check(r.status_code == 200, "guest gets a SHORT vort -> 200")

exit(0 if summary() else 1)
