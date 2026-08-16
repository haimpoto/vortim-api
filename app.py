from os import name

from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return { "status": "server is running" }, 200

if __name__ == "__main__":
    app.run(debug=True)

