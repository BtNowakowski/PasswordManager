import sqlite3


class DatabaseHelper:
    # initialize
    def __init__(self) -> None:
        self.TABLE_NAMES = ("passwords", "Users")
        self.DB_NAME = "database.db"
        self.connect = sqlite3.connect(self.DB_NAME)
        self.cursor = self.connect.cursor()

    # create the database table
    def createTable(self, table_name):
        if table_name == "passwords":
            self.cursor.execute(
                f"""CREATE TABLE IF NOT EXISTS {table_name}(id integer primary key not null, name TEXT, value TEXT, user_id INTEGER, FOREIGN KEY (user_id) REFERENCES users (id))"""
            )
        elif table_name == "users":
            self.cursor.execute(
                f"""CREATE TABLE IF NOT EXISTS {table_name}(id integer primary key not null, email TEXT, password TEXT, tfa BOOLEAN, tfa_key TEXT)"""
            )

    # this will help save the database after adding data to the database.
    # without this your data will not save and it might generate error when trying to assess the data
    def saveDatabase(self):
        self.connect.commit()

    def show_user_passwords(self, id):
        passwds = self.cursor.execute(
            f"SELECT passwords.id,passwords.name, passwords.value FROM passwords WHERE passwords.user_id = {id};"
        ).fetchall()
        return passwds

    # this will help close the database when you are done with it, to prevent data leek
    def closeConnection(self):
        self.connect.close()

    # this will retrieve all the data saved in the database in list format
    def selectAllFromDatabase(self, table_name):
        if table_name == "passwords":
            return self.cursor.execute(
                f"SELECT * FROM {self.TABLE_NAMES[0]}"
            ).fetchall()
        elif table_name == "users":
            return self.cursor.execute(
                f"SELECT * FROM {self.TABLE_NAMES[1]}"
            ).fetchall()

    # this will retrieve the first data that matches the query and return it as a data class
    def selectByName(self, name, table_name):
        if table_name == "passwords":
            data = self.cursor.execute(
                f"SELECT * FROM {self.TABLE_NAMES[0]} WHERE name=?", (name,)
            ).fetchone()
            return {
                "id": data[0],
                "name": data[1],
                "value": data[2],
                "user_id": data[3],
            }
        if table_name == "users":
            data = self.cursor.execute(
                f"SELECT * FROM {self.TABLE_NAMES[1]} WHERE email=?", (name,)
            ).fetchone()
            return {
                "id": data[0],
                "email": data[1],
                "password": data[2],
                "tfa": data[3],
                "tfa_key": data[4],
            }

    def selectById(self, id, table_name):
        if table_name == "passwords":
            data = self.cursor.execute(
                f"SELECT * FROM {self.TABLE_NAMES[0]} WHERE id=?", (id,)
            ).fetchone()
            return {
                "id": data[0],
                "email": data[1],
                "password": data[2],
                "tfa": data[3],
                "tfa_key": data[4],
            }
        elif table_name == "users":
            data = self.cursor.execute(
                f"SELECT * FROM {self.TABLE_NAMES[1]} WHERE id=?", (id,)
            ).fetchone()
            return {
                "id": data[0],
                "email": data[1],
                "password": data[2],
                "tfa": data[3],
                "tfa_key": data[4],
            }

    def UpdateById(self, value, id, table_name):
        if table_name == "passwords":
            self.cursor.execute(
                f"Update {self.TABLE_NAMES[0]} set value = ? where id = ?",
                (
                    value,
                    id,
                ),
            ).fetchone()
        elif table_name == "users":
            self.cursor.execute(
                f"UPDATE {self.TABLE_NAMES[1]} SET email = ? WHERE id=?",
                (
                    value,
                    id,
                ),
            ).fetchone()

    # this will delete all the data that matches the query
    def deleteByName(self, name, table_name):
        if table_name == "passwords":
            return self.cursor.execute(
                f"DELETE  FROM {self.TABLE_NAMES[0]} WHERE name=?", (name,)
            )
        elif table_name == "users":
            return self.cursor.execute(
                f"DELETE  FROM {self.TABLE_NAMES[1]} WHERE email=?", (name,)
            )

    # this will delete all the data that matches the query
    def deleteById(self, id, table_name):
        if table_name == "passwords":
            return self.cursor.execute(
                f"DELETE  FROM {self.TABLE_NAMES[0]} WHERE id=?", (id,)
            )
        elif table_name == "users":
            return self.cursor.execute(
                f"DELETE  FROM {self.TABLE_NAMES[1]} WHERE id=?", (id,)
            )

    # by using the data class, you can add stuff into the database
    def insertIntoDatabase(self, item, table_name):
        if table_name == "passwords":
            sql = f"INSERT INTO {self.TABLE_NAMES[0]} (name, value, user_id) VALUES (?, ?, ?)"
            val = (item.name, item.value, item.user_id)
            insert = self.cursor.execute(sql, val)
            self.connect.commit()
            return insert
        elif table_name == "users":
            sql = f"INSERT INTO {self.TABLE_NAMES[1]} (email, password, tfa, tfa_key) VALUES (?, ?, ?, ?)"
            val = (item.email, item.password, item.tfa, item.tfa_key)
            insert = self.cursor.execute(sql, val)
            self.connect.commit()
            return insert

    def checkIfEmailExists(self, email):
        data = self.cursor.execute(
            f"SELECT * FROM users WHERE email=?", (email,)
        ).fetchall()
        if len(data) == 0:
            return False
        else:
            return True

    def getUserTfaKey(self, id):
        data = self.cursor.execute(
            f"SELECT tfa_key FROM users WHERE id=?", (id,)
        ).fetchone()
        return data[0]

    def checkIfIdExists(self, id):
        data = self.cursor.execute(f"SELECT * FROM users WHERE id=?", (id,)).fetchall()
        if len(data) == 0:
            return False
        else:
            return True

    # this will not just delete all the data in the database, it will also delete the table as well
    def deleteDatabase(self, table_name):
        if table_name == "passwords":
            return self.cursor.execute(f"DROP TABLE IF EXISTS {self.TABLE_NAMES[0]}")
        elif table_name == "users":
            return self.cursor.execute(f"DROP TABLE IF EXISTS {self.TABLE_NAMES[1]}")

    def count_users(self):
        return self.cursor.execute(
            "SELECT COUNT(DISTINCT email) FROM users;"
        ).fetchone()[0]

    def get_user_id(self, email):
        return self.cursor.execute(
            f"SELECT id FROM {self.TABLE_NAMES[1]} WHERE email=?", (email,)
        ).fetchone()[0]
