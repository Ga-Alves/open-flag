import sqlite3


class Storage:
    def __init__(self):
        # Creates a connection with the database
        self.con = sqlite3.connect("./data.db")

    def __del__(self):
        # Finalizes the connection with the database
        self.con.close()

    def insert_flag(self, name: str, value: bool, description: str):
        # Creates a cursor for the transaction
        cur = self.con.cursor()

        # Executes the insertion
        try:
            entry = (name, value, description)
            cur.execute("INSERT INTO flags VALUES(?, ?, ?)", entry)
        except sqlite3.Error as error:
            return False

        # Commits and finalizes
        self.con.commit()
        cur.close()

        return True

    def update_flag(self, name: str, value: bool):
        # Creates a cursor for the transaction
        cur = self.con.cursor()

        # Executes the update
        try:
            entry = (value, name)
            cur.execute("UPDATE flags SET value=? WHERE name=?", entry)
        except sqlite3.Error as error:
            return False

        # Commits and finalizes
        self.con.commit()
        cur.close()

        return True

    def remove_flag(self, name: str):
        # Creates a cursor for the transaction
        cur = self.con.cursor()

        # Executes the removal
        try:
            entry = (name,)
            cur.execute("DELETE FROM flags WHERE name=?", entry)
        except sqlite3.Error as error:
            return False

        # Commits and finalizes
        self.con.commit()
        cur.close()

        return True

    def list_flags(self):
        # Creates a cursor for the transaction
        cur = self.con.cursor()

        # Executes the query
        try:
            res = cur.execute("SELECT name FROM flags")
            res = [entry[0] for entry in res.fetchall()]
        except sqlite3.Error as error:
            return False

        # Returns and finalizes
        cur.close()

        return res

    def get_flag(self, name: str):
        # Creates a cursor for the transaction
        cur = self.con.cursor()

        # Executes the query
        try:
            entry = (name,)
            res = cur.execute("SELECT * FROM flags WHERE name=?", entry)
            res = res.fetchone()
        except sqlite3.Error as error:
            return False

        # Returns value to bool due to sqlite converting it to integer
        if res:
            res = (res[0], bool(res[1]), res[2])

        # Returns and finalizes
        cur.close()

        return res
