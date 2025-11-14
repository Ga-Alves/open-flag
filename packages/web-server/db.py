import sqlite3
import json
import time


class Storage:

    COMPLETE = 0
    NOT_FOUND = -1
    DUPLICATE = -2

    def __init__(self, path="./data.db"):
        self.con = sqlite3.connect(path, check_same_thread=False)
        self.con.row_factory = sqlite3.Row
        self._create_table()
    
    def _create_table(self):
        """Cria a tabela se não existir"""
        with self.con:
            self.con.execute("""
                CREATE TABLE IF NOT EXISTS flags (
                    name TEXT PRIMARY KEY,
                    value INTEGER NOT NULL CHECK(value IN (0, 1)),
                    description TEXT,
                    usage_log TEXT NOT NULL DEFAULT '[]'
            )
        """)

    def __del__(self):
        # Finalizes the connection with the database
        self.con.close()

    def insert_flag(self, name: str, value: bool, description: str):
        with self.con as con:

            # Executes the insertion
            try:
                entry = (name, int(value), description, '[]')  # Array vazio inicial
                con.execute("INSERT INTO flags VALUES(?, ?, ?, ?)", entry)
            except sqlite3.IntegrityError as error:
                return (self.DUPLICATE, None)

            con.commit()

        return (self.COMPLETE, None)

    def log_date_time_for_flag(self, name: str):
        """
        Adiciona um timestamp atual ao log de uso da flag
        """
        with self.con as con:
        
            # Primeiro busca o log atual
            cur = con.execute("SELECT usage_log FROM flags WHERE name=?", (name,))
            result = cur.fetchone()
            
            if not result:
                return (self.NOT_FOUND, None)  # Flag não encontrada
            
            # Parse do JSON atual
            current_log = json.loads(result[0])
            
            # Adiciona o timestamp atual (em segundos desde epoch)
            current_timestamp = time.time()
            current_log.append(current_timestamp)
            
            # Atualiza no banco
            updated_log = json.dumps(current_log)
            con.execute("UPDATE flags SET usage_log=? WHERE name=?", (updated_log, name))
            
            con.commit()
        
        return (self.COMPLETE, current_timestamp)

    def get_flag_usage_log(self, name: str):
        """
        Retorna o array de timestamps de uso da flag
        """
        with self.con as con:
        
            cur = con.execute("SELECT usage_log FROM flags WHERE name=?", (name,))
            result = cur.fetchone()
            
            if not result:
                return (self.NOT_FOUND, None)  # Flag não encontrada
            
            usage_log = json.loads(result[0])
        
        return (self.COMPLETE, usage_log)

    # ATUALIZE o get_flag para incluir o usage_log no retorno
    def get_flag(self, name: str):
        with self.con as con:
            # Executes the query
            entry = (name,)
            res = con.execute("SELECT * FROM flags WHERE name=?", entry)
            res = res.fetchone()

            # If nothing was found (flag not found)
            if not res:
                return (self.NOT_FOUND, None)
            else:
                res = (
                    res[0],  # name
                    bool(res[1]),  # value
                    res[2],  # description
                    json.loads(res[3]) if res[3] else []  # usage_log (novo)
                )

        return (self.COMPLETE, res)

    def update_flag(self, currentName: str, newName: str, description: str):
        """
        Atualiza o nome e a descrição de uma flag existente
        """
        with self.con as con:

            # Executes the update
            try:
                entry = (newName, description, currentName)
                cur = con.execute("UPDATE flags SET name=?, description=? WHERE name=?", entry)
            except sqlite3.IntegrityError as error:
                return (self.DUPLICATE, None)  # Novo nome já existe

            # If nothing was changed (flag not found)
            if cur.rowcount == 0:
                return (self.NOT_FOUND, None)

            # Commits and finalizes
            con.commit()

        return (self.COMPLETE, None)


    def remove_flag(self, name: str):
        with self.con as con:

            # Executes the removal
            entry = (name,)
            cur = con.execute("DELETE FROM flags WHERE name=?", entry)

            # If nothing was changed (flag not found)
            if cur.rowcount == 0:
                return (self.NOT_FOUND, None)

            con.commit()

        return (self.COMPLETE, None)

    def list_flags(self):
        with self.con as con:

            # Executes the query - AGORA BUSCA TODOS OS CAMPOS
            res = con.execute("SELECT name, value, description, usage_log FROM flags")
            flags = []
            for entry in res.fetchall():
                flag_data = {
                    "name": entry[0],
                    "value": bool(entry[1]),
                    "description": entry[2],
                    "usage_log": json.loads(entry[3]) if entry[3] else []
                }
                flags.append(flag_data)

        return (self.COMPLETE, flags)
    def toggle_flag(self, name: str):
        """
        Inverte o valor de uma flag (true/false)
        """
        with self.con as con:

            # Primeiro busca o valor atual
            cur = con.execute("SELECT value FROM flags WHERE name=?", (name,))
            result = cur.fetchone()

            if not result:
                return (self.NOT_FOUND, None)  # Flag não encontrada

            # Inverte o valor
            current_value = bool(result[0])
            new_value = not current_value

            # Executes the update
            entry = (int(new_value), name)
            cur.execute("UPDATE flags SET value=? WHERE name=?", entry)

            con.commit()

        return (self.COMPLETE, new_value)