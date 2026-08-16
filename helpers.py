from config import *

from pathlib import Path
from flask import json
from pyluach import dates ,parshios



def parsha_exists(parsha_name: str) -> bool:
    parasha_path = Path(__file__).parent / "data" / "parshiot" / parsha_name
    return parasha_path.is_dir()


def load_vortim_for_parsha(parsha_name: str) -> list[dict[str, str]] | None:
    vortim = []
    parasha_path = Path(__file__).parent / "data" / "parshiot" / parsha_name
    if not parasha_path.exists():
        return None
    for vort in parasha_path.iterdir():
        if vort.is_file():
            with open(vort, "r", encoding="utf8") as file:
                the_vort = json.load(file)
                the_vort["is long"] = is_long(the_vort["text"])
                vortim.append(the_vort)
    return vortim


def load_single_vort(parsha_name: str, vort_id: str) -> dict[str, str] | None:
    parasha_path = Path(__file__).parent / "data" / "parshiot" / parsha_name
    if not parasha_path.exists():
        return None
    for vort in parasha_path.iterdir():
        if vort.is_file():
            with open(vort, "r", encoding="utf8") as file:
                the_vort = json.load(file)
                if the_vort["id"] == vort_id:
                    the_vort["is long"] = is_long(the_vort["text"])
                    return the_vort
    return None


def is_long(text: str) -> bool:
    return len(text.split("\n")) >= 20


def get_current_parsha() -> str | None:
    hebrew_parasha = parshios.getparsha_string(dates.GregorianDate.today(), israel=True, hebrew=True)
    return PARSHIOT_HEB_TO_ENG_SORTED[hebrew_parasha]
print(get_current_parsha())








"""
helpers.py — כל פונקציות העזר של הפרויקט נמצאות כאן בלבד.
app.py מייבא מכאן. אל תכתוב לוגיקה כבדה בתוך ה-routes עצמם.

הפונקציות שתבנה כאן לפי ההנחיות (השמות מופיעים במסמכי docs/):
  load_vortim_for_parsha(parsha_name)
  load_single_vort(parsha_name, vort_id)
  is_long(text)
  load_users() / save_users(users)
  load_admins()
  hash_password(password) / verify_password(password, hashed)
  create_token(username) / decode_token(token)
  get_current_parsha()
  validate_vort(data)
"""
