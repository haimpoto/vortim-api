"""
שלב 1 — כל ה-routes הבסיסיים עונים ב-JSON עם קוד 200.
"""
from _helpers import get, is_json, check, summary

print("STAGE 1 — basic routes")

r = get("/parshiot")
check(r.status_code == 200, "GET /parshiot -> 200")
check(is_json(r), "GET /parshiot returns JSON")

r = get("/parshiot/bereshit/vortim")
check(r.status_code == 200, "GET /parshiot/bereshit/vortim -> 200")
check(is_json(r), "vortim list returns JSON")

r = get("/parshiot/bereshit/vortim/vort_01")
check(r.status_code == 200, "GET single vort -> 200")
check(is_json(r), "single vort returns JSON")

r = get("/current")
check(r.status_code == 200, "GET /current -> 200")
check(is_json(r), "GET /current returns JSON")

exit(0 if summary() else 1)
