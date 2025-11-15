import sqlite3
import json
import time
import jwt
from datetime import datetime, timedelta, timezone
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash

JWT_SECRET = '2916b4f6-5e58-8327-b31b-d3852e15fa27'
JWT_EXPIRES_MINUTES = 60 * 24

class Storage:

    OK = 0
    NOT_FOUND = -1
    DUPLICATE = -2

    def __init__(self, path="./data.db"):
        self.con = sqlite3.connect(path, check_same_thread=False)
        self.con.row_factory = sqlite3.Row
        self.pw_hasher = PasswordHasher()  
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

            self.con.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    createdAt REAL NOT NULL
                )
            """)

    def __del__(self):
        # Finalizes the connection with the database
        self.con.close()

    ## ======================== FLAGS SERVICES ===========================

    def insert_flag(self, name: str, value: bool, description: str):
        with self.con as con:

            # Executes the insertion
            try:
                entry = (name, int(value), description, '[]')  # Array vazio inicial
                con.execute("INSERT INTO flags VALUES(?, ?, ?, ?)", entry)
            except sqlite3.IntegrityError as error:
                return (self.DUPLICATE, None)

            con.commit()

        return (self.OK, None)

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
        
        return (self.OK, current_timestamp)

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
        
        return (self.OK, usage_log)

    def get_flag(self, name: str):
        with self.con as con:
            con.row_factory = sqlite3.Row

            entry = (name,)
            res = con.execute("SELECT * FROM flags WHERE name=?", entry)
            res = res.fetchone()

            if not res:
                return (self.NOT_FOUND, None)
            
            flag = dict(res)
            flag["value"] = bool(flag["value"])
            flag["usage_log"] = json.loads(flag["usage_log"]) if flag["usage_log"] else []

        return (self.OK, flag)

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

        return (self.OK, None)


    def remove_flag(self, name: str):
        with self.con as con:

            # Executes the removal
            entry = (name,)
            cur = con.execute("DELETE FROM flags WHERE name=?", entry)

            # If nothing was changed (flag not found)
            if cur.rowcount == 0:
                return (self.NOT_FOUND, None)

            con.commit()

        return (self.OK, None)

    def list_flags(self):
        with self.con as con:
            con.row_factory = sqlite3.Row
            rows = con.execute("SELECT * FROM flags").fetchall()

        return (self.OK, rows)

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

        return (self.OK, new_value)
    
    ## ======================== USER SERVICES ===========================
    def create_user(self, name: str, email: str, password: str):
        """
        Cria um novo usuário com senha hasheada.
        Retorna DUPLICATE se email já existir.
        """
        with self.con as con:
            try:
                password_hash = self.pw_hasher.hash(password)
                con.execute(
                    "INSERT INTO users (name, email, password, createdAt) VALUES (?, ?, ?, ?)",
                    (name, email, password_hash, time.time())
                )
            except sqlite3.IntegrityError:
                return (self.DUPLICATE, None)

            con.commit()

        return (self.OK, None)

    def get_user(self, user_id: int = None, email: str = None):
        """
        Busca um usuário por ID OU email.
        """
        if not user_id and not email:
            raise ValueError("É necessário fornecer user_id ou email")

        with self.con as con:
            con.row_factory = sqlite3.Row
            if user_id:
                cur = con.execute("SELECT * FROM users WHERE id=?", (user_id,))
            else:
                cur = con.execute("SELECT * FROM users WHERE email=?", (email,))

            row = cur.fetchone()

            if not row:
                return (self.NOT_FOUND, None)

            return (self.OK, dict(row))

    def list_users(self):
        """
        Lista todos os usuários.
        """
        with self.con as con:
            con.row_factory = sqlite3.Row
            rows = con.execute("SELECT * FROM users").fetchall()
            return (self.OK, [dict(r) for r in rows])

    def update_user(self, user_id: int, name: str, email: str, password: str):
        """
        Atualiza campos de um usuário.
        Retorna DUPLICATE se o novo email já existir para outro usuário.
        """
        with self.con as con:
            try:
                # Verifica se queremos atualizar a senha ou manter a existente
                if password is None:
                    cur = con.execute("""
                        UPDATE users
                        SET name=?, email=?
                        WHERE id=?
                    """, (name, email, user_id))
                else:
                    password_hash = self.pw_hasher.hash(password)
                    cur = con.execute("""
                        UPDATE users
                        SET name=?, email=?, password=?
                        WHERE id=?
                    """, (name, email, password_hash, user_id))
            except sqlite3.IntegrityError:
                return (self.DUPLICATE, None)

            if cur.rowcount == 0:
                return (self.NOT_FOUND, None)

            con.commit()

        return (self.OK, None)

    def delete_user(self, user_id: int):
        """
        Remove um usuário pelo ID.
        """
        with self.con as con:
            cur = con.execute("DELETE FROM users WHERE id=?", (user_id,))

            if cur.rowcount == 0:
                return (self.NOT_FOUND, None)

            con.commit()

        return (self.OK, None)
    
    ## ======================== AUTH SERVICES ===========================
    def login(self, email: str, password: str):
        """
        Valida email e senha. Se correto, retorna um JWT.
        """
        code, user = self.get_user(None, email)

        if code != self.OK or user is None:
            raise ValueError("Invalid credentials")

        try:
            self.pw_hasher.verify(user["password"], password)
        except Exception:
            raise ValueError("Invalid credentials")

        # Cria o token JWT
        payload = {
            "sub": str(user["id"]),
            "email": user["email"],
            "exp": datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRES_MINUTES)
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
        return token
    
    def validate_token(self, token: str):
        """
        Retorna o payload decodificado se o JWT for válido,
        senão lança ValueError.
        """
        try:
            print(f'token: {token}')
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            print(f'payload: {payload}')
            return payload
        except jwt.ExpiredSignatureError as e:
            print(f'Erro de expiração: {e}')
            raise ValueError("Token expired")
        except jwt.InvalidTokenError as e:
            print(f'Erro de token inválido: {e}')
            raise ValueError("Invalid token")
        except Exception as e:
            print(f'Erro inesperado: {type(e).__name__}: {e}')
            raise

