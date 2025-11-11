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
        except sqlite3.IntegrityError as error:
            return -2

        # Commits and finalizes
        self.con.commit()
        cur.close()

        return 0

    def update_flag(self, name: str, value: bool):
        # Creates a cursor for the transaction
        cur = self.con.cursor()

        # Executes the update
        entry = (value, name)
        cur.execute("UPDATE flags SET value=? WHERE name=?", entry)

        # If nothing was changed (flag not found)
        if cur.rowcount == 0:
            return -1

        # Commits and finalizes
        self.con.commit()
        cur.close()

        return 0

    def remove_flag(self, name: str):
        # Creates a cursor for the transaction
        cur = self.con.cursor()

        # Executes the removal
        entry = (name,)
        cur.execute("DELETE FROM flags WHERE name=?", entry)

        # If nothing was changed (flag not found)
        if cur.rowcount == 0:
            return -1

        # Commits and finalizes
        self.con.commit()
        cur.close()

        return 0

    def list_flags(self):
        # Creates a cursor for the transaction
        cur = self.con.cursor()

        # Executes the query
        res = cur.execute("SELECT name FROM flags")
        res = [entry[0] for entry in res.fetchall()]

        # Returns and finalizes
        cur.close()

        return res

    def get_flag(self, name: str):
        # Creates a cursor for the transaction
        cur = self.con.cursor()

        # Executes the query
        entry = (name,)
        res = cur.execute("SELECT * FROM flags WHERE name=?", entry)
        res = res.fetchone()

        # If nothing was found (flag not found)
        if not res:
            return -1
        else:
            res = (
                res[0],
                bool(res[1]),
                res[2],
            )  # Returns value to bool due to sqlite converting it to integer

        # Returns and finalizes
        cur.close()

        return res
