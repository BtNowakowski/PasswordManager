from passlib.hash import pbkdf2_sha256
from user import User
from database import DatabaseHelper


def register(email, passwd, tfa=False):
    db = DatabaseHelper()
    if not db.checkIfEmailExists(email) and not db.checkIfIdExists(
        db.count_users() + 1
    ):
        hash_pass = pbkdf2_sha256.hash(passwd)
        id = db.count_users() + 1
        user = User(id, email, hash_pass, tfa)
        db.insertIntoDatabase(user, "users")
        db.saveDatabase()
        db.closeConnection()
        return user
    else:
        return None
