"""
שלב 2 — קריאת וורטים אמיתיים מהקבצים, שדה is_long, וטיפול ב-404.
"""
from _helpers import get, is_json, check, summary

print("STAGE 2 — read from files")

r = get("/parshiot/bereshit/vortim")
check(r.status_code == 200, "existing parsha -> 200")
data = r.json() if is_json(r) else []
check(isinstance(data, list) and len(data) > 0, "returns a non-empty list of vortim")
if data:
    v = data[0]
    check("id" in v and "title" in v and "text" in v, "vort has id/title/text")
    check("is_long" in v, "vort has computed is_long field")

r = get("/parshiot/noach/vortim")
check(r.status_code == 200, "second parsha (noach) -> 200")

r = get("/parshiot/does_not_exist/vortim")
check(r.status_code == 404, "unknown parsha -> 404")

r = get("/parshiot/bereshit/vortim/nope_999")
check(r.status_code == 404, "unknown vort id -> 404")

exit(0 if summary() else 1)
