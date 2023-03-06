import sqlite3

def init_db():
    with open('schema.sql', 'r') as sql_file:
        sql_script = sql_file.read()
    db = sqlite3.connect('sqlite.db')
    cursor = db.cursor()
    cursor.executescript(sql_script)
    db.commit()
    db.close()


class DatabaseConnection:
    def __init__(self):
        self.db = sqlite3.connect("./database/sqlite.db")
        self.cursor = self.db.cursor()

    def get_user_password(self,username):
        return self.cursor.execute("SELECT password FROM users WHERE username=?",(username,)).fetchone()
    def check_if_already_challenge(self,username):
        return self.get_challenge(username) is not None

    def insert_challenge(self, username, challenge, plaintext):
        if not self.check_if_already_challenge(username):
            self.cursor.execute("INSERT INTO challenges (username,challenge,plaintext) VALUES(?,?,?)",(username,challenge,plaintext))
            self.db.commit()

    def get_challenge(self, username):
        return self.cursor.execute("SELECT challenge FROM challenges WHERE username=?",(username,)).fetchone()

    def remove_challenge(self,username):
        self.cursor.execute("DELETE FROM challenges WHERE username=?",(username,))
        self.db.commit()
    def get_auth_token(self, username):
        return self.cursor.execute("SELECT challenge FROM challenges WHERE username=?", (username,)).fetchone()

    def get_plaintext(self,username):
        return self.cursor.execute("SELECT plaintext FROM challenges WHERE username=?",(username,)).fetchone()

    def insert_token(self,username,token, expiration):
        self.cursor.execute("INSERT INTO tokens (username,token,expiration) VALUES (?,?,?)",(username,token,expiration))
        self.db.commit()