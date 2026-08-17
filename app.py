from flask import Flask, request
import helpers
import config

app = Flask(__name__)


@app.route("/")
def home():
    return {"status": "server is running"}, 200


@app.route("/parshiot")
def get_parshiot() -> tuple[list[str], int]:
    return list(config.PARSHIOT_HEB_TO_ENG_SORTED.values()), 200


@app.route("/parshiot/<parsha_name>/vortim")
def get_vortim_by_parasha(parsha_name: str) -> tuple[list[dict[str, str]] | dict[str, str], int]:
    vortim = helpers.load_vortim_for_parsha(parsha_name)
    if vortim is None:
        return {"error": f"{parsha_name} is not exists"}, 404
    return vortim, 200


@app.route("/parshiot/<parsha_name>/vortim/<vort_id>")
def get_vort_by_parasha_by_id(parsha_name: str, vort_id: str) -> tuple[dict[str, str], int]:
    if not helpers.parsha_exists(parsha_name):
        return {"error": f"{parsha_name} is not exists"}, 404
    vort = helpers.load_single_vort(parsha_name, vort_id)
    if vort is None:
        return {"error": f"{vort_id} is not exist"}, 404
    return vort, 200


@app.route("/current")
def get_current_parasha() -> tuple[str | dict[str, str], int]:
    parasha = helpers.get_current_parsha()
    if parasha is None:
        return {"error": "no parasha"}, 400
    return parasha, 200


@app.route("/current/vortim")
def get_vortim_by_current_parasha() -> tuple[list[dict[str, str]] | dict[str, str], int]:
    parasha = helpers.get_current_parsha()
    if parasha is None:
        return {"error": "no parasha"}, 400
    vortim = helpers.load_vortim_for_parsha(parasha)
    if vortim is None:
        return {"error": f"{parasha} does not has vortim"}, 404
    return vortim, 200


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    if not data or "username" not in data or "password" not in data:
        return {"error": "username and password are required"}, 400
    username = data["username"]
    password = data["password"]
    users = helpers.load_users()
    for user in users:
        if user["username"] == username:
            return {"error": "user already exists"}, 400
    hashed_password = helpers.hash_password(password)
    users.append({"username": username, "password": hashed_password})
    helpers.save_users(users)
    return {"message": "User registered successfully"}, 201


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if not data or "username" not in data or "password" not in data:
        return {"error": "username and password are required"}, 400
    username = data["username"]
    password = data["password"]
    users = helpers.load_users()
    for user in users:
        if user["username"] == username:
            if helpers.verify_password(password, user["password"]):
                token = helpers.create_token(username)
                return {"token": token}, 200
            else:
                return {"error": "Invalid password"}, 401
    return {"error": "User not found"}, 401


if __name__ == "__main__":
    app.run(debug=True)
