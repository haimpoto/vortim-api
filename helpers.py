from pathlib import Path
from flask import json
from pyluach import dates, parshios
import bcrypt
import config
import jwt
import datetime


def parsha_exists(parsha_name: str) -> bool:
    parasha_path = Path(__file__).parent / "data" / "parshiot" / parsha_name
    return parasha_path.is_dir()


def load_vortim_for_parsha(parsha_name: str) -> list[dict[str, str]] | None:
    vortim = []
    parasha_path = Path(__file__).parent / "data" / "parshiot" / parsha_name
    if not parasha_path.exists():
        return None
    for vort in parasha_path.iterdir():
        if vort.is_file() and vort.suffix == ".json":
            with open(vort, "r", encoding="utf8") as file:
                the_vort = json.load(file)
                the_vort["is long"] = is_long(the_vort["text"])
                vortim.append(the_vort)
    if not vortim:
        return None
    return vortim


def load_single_vort(parsha_name: str, vort_id: str) -> dict[str, str] | None:
    parasha_path = Path(__file__).parent / "data" / "parshiot" / parsha_name
    if not parasha_path.exists():
        return None
    for vort in parasha_path.iterdir():
        if vort.is_file() and vort.suffix == ".json":
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
    return config.PARSHIOT_HEB_TO_ENG_SORTED.get(hebrew_parasha)


def hash_password(password: str) -> str:
    hashed_password = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())
    return hashed_password.decode("utf8")


def load_users() -> list[dict]:
    users_path = Path(__file__).parent / "data" / "users.json"
    if not users_path.exists():
        return []
    with open(users_path, "r", encoding="utf8") as file:
        return json.load(file)


def save_users(users: list[dict]):
    users_path = Path(__file__).parent / "data" / "users.json"
    with open(users_path, "w", encoding="utf8") as file:
        json.dump(users, file, indent=4)


def verify_password(password: str, hashed: str) -> bool:
    encoded_password = password.encode('utf-8')
    encoded_hashed = hashed.encode('utf-8')
    return bcrypt.checkpw(encoded_password, encoded_hashed)


def create_token(username: str) -> str:
    payload = {
        "username": username,
        "exp": datetime.datetime.now() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, config.SECRET_KEY, algorithm="HS256")


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
