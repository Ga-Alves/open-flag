import sqlite3
import json
import time
import jwt
from datetime import datetime, timedelta, timezone
from argon2 import PasswordHasher

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

    # =====================================================================
    # DATABASE INITIALIZATION
    # =====================================================================

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

        # Garantir a criação do usuário admin
        self._ensure_admin_exists()

    def _ensure_admin_exists(self):
        """Garante que exista um usuário admin padrão persistente."""
        admin_email = "admin@admin.com"
        admin_password = "admin123"

        code, user = self.get_user(email=admin_email)

        if code == self.OK and user is not None:
            return  # Admin já existe

        print("⚠️ Usuário admin não encontrado. Criando admin padrão...")

        password_hash = self.pw_hasher.hash(admin_password)

        with self.con:
            self.con.execute("""
                INSERT INTO users (name, email, password, createdAt)
                VALUES (?, ?, ?, ?)
            """, ("Admin", admin_email, password_hash, time.time()))
            self.con.commit()

        print("✅ Usuário admin criado:")
        print("   email: admin@admin.com")
        print("   senha: admin123")

    def __del__(self):
        self.con.close()

    # =====================================================================
    # FLAG SERVICES
    # =====================================================================

    def insert_flag(self, name: str, value: bool, description: str):
        with self.con as con:
            try:
                entry = (name, int(value), description, '[]')
                con.execute("INSERT INTO flags VALUES(?, ?, ?, ?)", entry)
            except sqlite3.IntegrityError:
                return (self.DUPLICATE, None)

            con.commit()

        return (self.OK, None)

    def log_date_time_for_flag(self, name: str):
        with self.con as con:
            cur = con.execute("SELECT usage_log FROM flags WHERE name=?", (name,))
            result = cur.fetchone()

            if not result:
                return (self.NOT_FOUND, None)

            current_log = json.loads(result[0])
            current_timestamp = time.time()
            current_log.append(current_timestamp)

            con.execute(
                "UPDATE flags SET usage_log=? WHERE name=?",
                (json.dumps(current_log), name)
            )
            con.commit()

        return (self.OK, current_timestamp)

    def get_flag_usage_log(self, name: str):
        with self.con as con:
            cur = con.execute("SELECT usage_log FROM flags WHERE name=?", (name,))
            result = cur.fetchone()

            if not result:
                return (self.NOT_FOUND, None)

            usage_log = json.loads(result[0])

        return (self.OK, usage_log)

    def get_flag(self, name: str):
        with self.con as con:
            res = con.execute("SELECT * FROM flags WHERE name=?", (name,)).fetchone()

            if not res:
                return (self.NOT_FOUND, None)

            flag = dict(res)
            flag["value"] = bool(flag["value"])
            flag["usage_log"] = json.loads(flag["usage_log"])

        return (self.OK, flag)

    def update_flag(self, currentName: str, newName: str, description: str):
        with self.con as con:
            try:
                cur = con.execute(
                    "UPDATE flags SET name=?, description=? WHERE name=?",
                    (newName, description, currentName)
                )
            except sqlite3.IntegrityError:
                return (self.DUPLICATE, None)

            if cur.rowcount == 0:
                return (self.NOT_FOUND, None)

            con.commit()

        return (self.OK, None)

    def remove_flag(self, name: str):
        with self.con as con:
            cur = con.execute("DELETE FROM flags WHERE name=?", (name,))

            if cur.rowcount == 0:
                return (self.NOT_FOUND, None)

            con.commit()

        return (self.OK, None)

    def list_flags(self):
        with self.con as con:
            return (self.OK, con.execute("SELECT * FROM flags").fetchall())

    def toggle_flag(self, name: str):
        with self.con as con:
            cur = con.execute("SELECT value FROM flags WHERE name=?", (name,))
            result = cur.fetchone()

            if not result:
                return (self.NOT_FOUND, None)

            new_value = not bool(result[0])

            con.execute(
                "UPDATE flags SET value=? WHERE name=?",
                (int(new_value), name)
            )
            con.commit()

        return (self.OK, new_value)

    # =====================================================================
    # USER SERVICES
    # =====================================================================

    def create_user(self, name: str, email: str, password: str):
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
        if not user_id and not email:
            raise ValueError("É necessário fornecer user_id ou email")

        with self.con as con:
            if user_id:
                cur = con.execute("SELECT * FROM users WHERE id=?", (user_id,))
            else:
                cur = con.execute("SELECT * FROM users WHERE email=?", (email,))

            row = cur.fetchone()

            if not row:
                return (self.NOT_FOUND, None)

            return (self.OK, dict(row))

    def list_users(self):
        with self.con as con:
            rows = con.execute("SELECT * FROM users").fetchall()
            return (self.OK, [dict(r) for r in rows])

    def update_user(self, user_id: int, name: str, email: str, password: str):
        with self.con as con:
            try:
                if password is None:
                    cur = con.execute(
                        "UPDATE users SET name=?, email=? WHERE id=?",
                        (name, email, user_id)
                    )
                else:
                    password_hash = self.pw_hasher.hash(password)
                    cur = con.execute(
                        "UPDATE users SET name=?, email=?, password=? WHERE id=?",
                        (name, email, password_hash, user_id)
                    )
            except sqlite3.IntegrityError:
                return (self.DUPLICATE, None)

            if cur.rowcount == 0:
                return (self.NOT_FOUND, None)

            con.commit()

        return (self.OK, None)

    def delete_user(self, user_id: int):
        with self.con as con:
            cur = con.execute("DELETE FROM users WHERE id=?", (user_id,))

            if cur.rowcount == 0:
                return (self.NOT_FOUND, None)

            con.commit()

        return (self.OK, None)

    # =====================================================================
    # AUTH SERVICES
    # =====================================================================

    def login(self, email: str, password: str):
        code, user = self.get_user(email=email)

        if code != self.OK or user is None:
            raise ValueError("Invalid credentials")

        try:
            self.pw_hasher.verify(user["password"], password)
        except Exception:
            raise ValueError("Invalid credentials")

        payload = {
            "sub": str(user["id"]),
            "email": user["email"],
            "exp": datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRES_MINUTES)
        }

        return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    def validate_token(self, token: str):
        try:
            return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")
