from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/search/<name>", methods=["GET"])
def search(name):
    pass


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
