from flask import Flask, request
from authentWizard import get_challenge, validate_challenge, generate_auth_token, validate_given_token

app = Flask(__name__)


@app.route("/login", methods=['POST'])
def login():
    username = request.data['username']
    return get_challenge(username)


@app.route("/login/result", methods=['POST'])
def login_results():
    res = request.data['res']
    if validate_challenge(res) is not None:
        return generate_auth_token()
    return ""


@app.route("/validate_token", methods=['POST'])
def validate_token():
    token = request.data['token']
    if validate_given_token(token):
        return {'validate': True}
    return {'validate': False}


if __name__ == "__main__":
    app.run(debug=True)
