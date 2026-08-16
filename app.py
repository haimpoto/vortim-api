from os import name

from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return { "status": "server is running" }, 200


@app.route("/parshiot")
def get_parshiot() -> dict[str, str]:
    return {"parshiot": "parshiot"}


@app.route("/parshiot/<parsha>/vortim")
def get_vortim_by_parasha(parsha: str) -> dict[str, str]:
    return {"vortim": "vortim"}


@app.route("/parshiot/<parsha>/vortim/<int:vort_id>")
def get_vort_by_parasha_by_id(parsha: str, vort_id: int) -> dict[str, str]:
    return {"vort": "vort"}

@app.route("/current")
def get_current_parasha():
    return {"parasha": "parasha"}


if __name__ == "__main__":
    app.run(debug=True)

