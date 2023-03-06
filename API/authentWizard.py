import string
import random
import hashlib
from Crypto.Cipher import AES
from database.database import DatabaseConnection


def generate_challenge(username):
    password = DatabaseConnection().get_user_password(username)
    if password is not None:
        letters = string.ascii_letters + string.digits
        random_str = ''.join(random.choice(letters) for _ in range(64))
        enc = enc_challenge(password[0], random_str)
        DatabaseConnection().insert_challenge(username, enc, random_str)
        return enc
    return None


def enc_challenge(password, random_string):
    key = hashlib.md5(password.encode()).hexdigest().encode()
    cipher = AES.new(key, AES.MODE_ECB)
    enc = cipher.encrypt(random_string.encode())
    return enc


def generate_auth_token(username):
    letters = string.ascii_letters + string.digits
    auth_token = username + ':' + ''.join(random.choice(letters) for _ in range(64))
    return auth_token


def validate_challenge(username, challenge):
    db_challenge = DatabaseConnection().get_plaintext(username)
    if db_challenge is not None and challenge == db_challenge[0]:
        DatabaseConnection().remove_challenge(username)
        auth_token = generate_auth_token(username)
        DatabaseConnection().insert_token(username,auth_token,9999999)
        return
    else:
        DatabaseConnection().remove_challenge(username)
        return None


def validate_given_token(username, token):
    db_token = DatabaseConnection().get_auth_token(username)
    if db_token is not None:
        return db_token[0] == token
    return False
