import helpers
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return { "status": "server is running" }, 200


@app.route("/parshiot")
def get_parshiot() -> dict[str, str]:
    return {"parshiot": "parshiot"}


@app.route("/parshiot/<parsha_name>/vortim")
def get_vortim_by_parasha(parsha_name: str) -> tuple[list[dict[str, str]] | dict[str, str], int]:
    vortim = helpers.load_vortim_for_parsha(parsha_name)
    if not vortim:
        return {"error": f"{parsha_name}is not exists"}, 404
    return vortim, 200


@app.route("/parshiot/<parsha_name>/vortim/<vort_id>")
def get_vort_by_parasha_by_id(parsha_name: str, vort_id: str):
    vort = helpers.load_single_vort(parsha_name, vort_id)
    if isinstance(vort, str):
        return {"error": vort}, 404
    return vort


@app.route("/current")
def get_current_parasha():
    return {"parasha": "parasha"}


if __name__ == "__main__":
    app.run(debug=True)

