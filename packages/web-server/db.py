import sqlite3
import json
import time


class Storage:
    def __init__(self):
        # Creates a connection with the database
        self.con = sqlite3.connect("./data.db", check_same_thread=False)
        self._create_table()
    
    def _create_table(self):
        """Cria a tabela se não existir"""
        cur = self.con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS flags (
                name TEXT PRIMARY KEY,
                value INTEGER,
                description TEXT,
                usage_log TEXT  -- NOVO CAMPO: array de timestamps em JSON
            )
        """)
        self.con.commit()
        cur.close()

    def __del__(self):
        # Finalizes the connection with the database
        self.con.close()

    def insert_flag(self, name: str, value: bool, description: str):
        # Creates a cursor for the transaction
        cur = self.con.cursor()

        # Executes the insertion
        try:
            entry = (name, int(value), description, '[]')  # Array vazio inicial
            cur.execute("INSERT INTO flags VALUES(?, ?, ?, ?)", entry)
        except sqlite3.IntegrityError as error:
            return (-2, None)

        # Commits and finalizes
        self.con.commit()
        cur.close()

        return (0, None)

    def log_date_time_for_flag(self, name: str):
        """
        Adiciona um timestamp atual ao log de uso da flag
        """
        cur = self.con.cursor()
        
        # Primeiro busca o log atual
        cur.execute("SELECT usage_log FROM flags WHERE name=?", (name,))
        result = cur.fetchone()
        
        if not result:
            return (-1, None)  # Flag não encontrada
        
        # Parse do JSON atual
        current_log = json.loads(result[0])
        
        # Adiciona o timestamp atual (em segundos desde epoch)
        current_timestamp = time.time()
        current_log.append(current_timestamp)
        
        # Atualiza no banco
        updated_log = json.dumps(current_log)
        cur.execute("UPDATE flags SET usage_log=? WHERE name=?", (updated_log, name))
        
        # Commits and finalizes
        self.con.commit()
        cur.close()
        
        return (0, current_timestamp)

    def get_flag_usage_log(self, name: str):
        """
        Retorna o array de timestamps de uso da flag
        """
        cur = self.con.cursor()
        
        cur.execute("SELECT usage_log FROM flags WHERE name=?", (name,))
        result = cur.fetchone()
        
        if not result:
            return (-1, None)  # Flag não encontrada
        
        usage_log = json.loads(result[0])
        cur.close()
        
        return (0, usage_log)

    # ATUALIZE o get_flag para incluir o usage_log no retorno
    def get_flag(self, name: str):
        # Creates a cursor for the transaction
        cur = self.con.cursor()

        # Executes the query
        entry = (name,)
        res = cur.execute("SELECT * FROM flags WHERE name=?", entry)
        res = res.fetchone()

        # If nothing was found (flag not found)
        if not res:
            return (-1, None)
        else:
            res = (
                res[0],  # name
                bool(res[1]),  # value
                res[2],  # description
                json.loads(res[3]) if res[3] else []  # usage_log (novo)
            )

        # Returns and finalizes
        cur.close()

        return (0, res)

    def update_flag(self, currentName: str, newName: str, description: str):
        """
        Atualiza o nome e a descrição de uma flag existente
        """
        # Creates a cursor for the transaction
        cur = self.con.cursor()

        # Executes the update
        try:
            entry = (newName, description, currentName)
            cur.execute("UPDATE flags SET name=?, description=? WHERE name=?", entry)
        except sqlite3.IntegrityError as error:
            return (-2, None)  # Novo nome já existe

        # If nothing was changed (flag not found)
        if cur.rowcount == 0:
            return (-1, None)

        # Commits and finalizes
        self.con.commit()
        cur.close()

        return (0, None)


    def remove_flag(self, name: str):
        # Creates a cursor for the transaction
        cur = self.con.cursor()

        # Executes the removal
        entry = (name,)
        cur.execute("DELETE FROM flags WHERE name=?", entry)

        # If nothing was changed (flag not found)
        if cur.rowcount == 0:
            return (-1, None)

        # Commits and finalizes
        self.con.commit()
        cur.close()

        return (0, None)

    def list_flags(self):
        # Creates a cursor for the transaction
        cur = self.con.cursor()

        # Executes the query - AGORA BUSCA TODOS OS CAMPOS
        res = cur.execute("SELECT name, value, description, usage_log FROM flags")
        flags = []
        for entry in res.fetchall():
            flag_data = {
                "name": entry[0],
                "value": bool(entry[1]),
                "description": entry[2],
                "usage_log": json.loads(entry[3]) if entry[3] else []
            }
            flags.append(flag_data)

        # Returns and finalizes
        cur.close()

        return (0, flags)
    def toggle_flag(self, name: str):
        """
        Inverte o valor de uma flag (true/false)
        """
        # Creates a cursor for the transaction
        cur = self.con.cursor()

        # Primeiro busca o valor atual
        cur.execute("SELECT value FROM flags WHERE name=?", (name,))
        result = cur.fetchone()

        if not result:
            return (-1, None)  # Flag não encontrada

        # Inverte o valor
        current_value = bool(result[0])
        new_value = not current_value

        # Executes the update
        entry = (int(new_value), name)
        cur.execute("UPDATE flags SET value=? WHERE name=?", entry)

        # Commits and finalizes
        self.con.commit()
        cur.close()

        return (0, new_value)