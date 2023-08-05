# from modules.interface import app
from interface import app
from database import DatabaseHelper as Db

dba = Db()

if __name__ == "__main__":
    dba.createTable("passwords")
    dba.createTable("users")

    app.mainloop()
