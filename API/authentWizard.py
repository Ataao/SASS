import string
import random
import hashlib
from Crypto.Cipher import AES
from database import insert_challenge, get_challenge, get_auth_token


def generate_challenge():
    letters = string.ascii_letters + string.digits
    random_str = ''.join(random.choice(letters) for _ in range(64))
    enc = enc_challenge("password", random_str)
    insert_challenge("username", enc)


def enc_challenge(password, random_string):
    key = hashlib.md5(password.encode()).hexdigest().encode()
    cipher = AES.new(key, AES.MODE_ECB)
    enc = cipher.encrypt(random_string.encode())
    dec = cipher.decrypt(enc)
    return enc


def generate_auth_token(username):
    letters = string.ascii_letters + string.digits
    auth_token = username + ':' + ''.join(random.choice(letters) for _ in range(64))
    return auth_token


def validate_challenge(username, challenge):
    db_challenge = get_challenge(username)
    if challenge == db_challenge:
        return generate_auth_token(username)
    else:
        return None


def validate_given_token(username, token):
    return get_auth_token(username) == token


get_challenge("username")
