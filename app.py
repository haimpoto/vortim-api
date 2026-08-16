from flask import Flask
import helpers
import config

app = Flask(__name__)


@app.route("/")
def home():
    return { "status": "server is running" }, 200


@app.route("/parshiot")
def get_parshiot() -> list[str]:
    return [config.PARSHIOT_HEB_TO_ENG_SORTED[parasha_name] for parasha_name in config.PARSHIOT_HEB_TO_ENG_SORTED]


@app.route("/parshiot/<parsha_name>/vortim")
def get_vortim_by_parasha(parsha_name: str) -> tuple[list[dict[str, str]] | dict[str, str], int]:
    vortim = helpers.load_vortim_for_parsha(parsha_name)
    if vortim is None:
        return {"error": f"{parsha_name} is not exists"}, 404
    return vortim, 200


@app.route("/parshiot/<parsha_name>/vortim/<vort_id>")
def get_vort_by_parasha_by_id(parsha_name: str, vort_id: str):
    if not helpers.parsha_exists(parsha_name):
        return {"error": f"{parsha_name} is not exists"}, 404
    vort = helpers.load_single_vort(parsha_name, vort_id)
    if vort is None:
        return {"error": f"{vort_id} is not exist"}, 404
    return vort, 200


@app.route("/current")
def get_current_parasha():
    return helpers.get_current_parsha()


@app.route("/current/vortim")
def get_vortim_by_current_parasha():
    return get_vortim_by_parasha(helpers.get_current_parsha())


if __name__ == "__main__":
    app.run(debug=True)
