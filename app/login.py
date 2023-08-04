from passlib.hash import pbkdf2_sha256
from user import User
from database import DatabaseHelper


def login(email, password):
    db = DatabaseHelper()
    if db.checkIfEmailExists(email):
        users = db.selectAllFromDatabase("users")
        for user in users:
            if user[1] == email and pbkdf2_sha256.verify(password, user[2]):
                return {
                    "id": user[0],
                    "email": user[1],
                    "password": user[2],
                    "tfa": user[3],
                    "tfa_key": user[4],
                }
        return None
    db.closeConnection()
