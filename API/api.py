from flask import Flask, request
from authentWizard import generate_challenge, validate_challenge, generate_auth_token, validate_given_token

app = Flask(__name__)


@app.route("/login", methods=['POST'])
def login():
    return generate_challenge(request.json["username"])


@app.route("/login/result", methods=['POST'])
def login_results():
    if validate_challenge(request.json['username'],request.json['res']) is not None:
        return generate_auth_token(request.json['username'])
    return ""


@app.route("/validate_token", methods=['POST'])
def validate_token():
    if validate_given_token(request.json["token"]):
        return {'validate': True}
    return {'validate': False}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
