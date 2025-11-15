import pytest
import json
import time
from fastapi.testclient import TestClient
from unittest.mock import patch
import uuid

from db import Storage
from server import app

# ============================================================
# FIXTURE: cria banco em memória para mockar o SQLite
# ============================================================
@pytest.fixture(autouse=True)
def mock_storage(monkeypatch):
    """
    Sobrescreve server.storage com um Storage em memória.
    """
    test_storage = Storage()            # usa sqlite normal
    test_storage.con = test_storage.con = __import__("sqlite3").connect(":memory:", check_same_thread=False)
    test_storage._create_table()

    # 👉 monkeypatcha o storage global usado pelo servidor
    monkeypatch.setattr("server.storage", test_storage)

    return test_storage

# ============================================================
# HELPERS PARA AUTENTICAÇÃO
# ============================================================
def create_user_and_login(client, name="John"):
    email = f"user_{uuid.uuid4()}@example.com"
    password = str(uuid.uuid4())

    res = client.post("/users", json={
        "name": name,
        "email": email,
        "password": password
    })
    assert res.status_code == 201

    login = client.post("/login", json={
        "email": email,
        "password": password
    })
    assert login.status_code == 200
    token = login.json()["token"]

    return token

def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}

# ============================================================
# CLIENT FastAPI
# ============================================================
client = TestClient(app)


# ============================================================
# TESTES DE FLAGS
# ============================================================

def test_create_flag_success():
    token = create_user_and_login(client)
    response = client.post("/flags", json={
        "name": "flag1",
        "value": True,
        "description": "desc 1"
    }, headers=auth_headers(token))
    assert response.status_code == 201
    assert response.json()["name"] == "flag1"


def test_create_flag_duplicate():
    token = create_user_and_login(client)
    # cria a primeira
    client.post("/flags", json={
        "name": "flag1",
        "value": True,
        "description": "desc 1"
    }, headers=auth_headers(token))
    # tenta duplicar
    response = client.post("/flags", json={
        "name": "flag1",
        "value": False,
        "description": "other desc"
    }, headers=auth_headers(token))
    assert response.status_code == 500
    assert "already exists" in response.json()["detail"]


def test_list_flags():
    token = create_user_and_login(client)
    # insere duas flags
    client.post("/flags", json={"name": "flag1", "value": True, "description": "d1"}, headers=auth_headers(token))
    client.post("/flags", json={"name": "flag2", "value": False, "description": "d2"}, headers=auth_headers(token))

    res = client.get("/flags")
    assert res.status_code == 200
    flags = res.json()
    assert len(flags) == 2
    assert flags[0]["name"] in ["flag1", "flag2"]
    assert flags[1]["name"] in ["flag1", "flag2"]


def test_get_flag_and_log_usage():
    token = create_user_and_login(client)
    client.post("/flags", json={"name": "flagX", "value": True, "description": "test log"}, headers=auth_headers(token))

    res1 = client.get("/flags/flagX")
    assert res1.status_code == 200
    flag = res1.json()

    assert flag["name"] == "flagX"      # name
    assert flag["value"] is True        # value
    assert flag["description"] == "test log"
    assert isinstance(flag["usage_log"], list)

    # deve ter 1 registro de uso
    assert len(flag["usage_log"]) == 1

    # chama de novo → outro timestamp
    res2 = client.get("/flags/flagX")
    flag2 = res2.json()
    assert len(flag2["usage_log"]) == 2


def test_get_flag_not_found():
    res = client.get("/flags/does_not_exist")
    assert res.status_code == 404


def test_toggle_flag():
    token = create_user_and_login(client)
    client.post("/flags", json={"name": "flagY", "value": True, "description": ""}, headers=auth_headers(token))

    res = client.put("/flags/flagY/toggle", headers=auth_headers(token))
    assert res.status_code == 200
    assert res.json()["new_value"] is False

    res = client.put("/flags/flagY/toggle", headers=auth_headers(token))
    assert res.json()["new_value"] is True


def test_toggle_not_found():
    token = create_user_and_login(client)
    res = client.put("/flags/noFlag/toggle", headers=auth_headers(token))
    assert res.status_code == 404


def test_update_flag_success():
    token = create_user_and_login(client)
    client.post("/flags",
                json={"name": "oldName", "value": True, "description": "old"},
                headers=auth_headers(token))

    res = client.put("/flags/oldName", json={
        "name": "newName",
        "description": "updated description"
    }, headers=auth_headers(token))

    assert res.status_code == 200

    # checar se atualizou mesmo
    get_res = client.get("/flags/newName")
    assert get_res.status_code == 200
    flag = get_res.json()
    assert flag["name"] == "newName"
    assert flag["description"] == "updated description"


def test_update_flag_not_found():
    token = create_user_and_login(client)
    res = client.put("/flags/ghost", json={
        "name": "anything",
        "description": "..."
    }, headers=auth_headers(token))
    assert res.status_code == 404


def test_update_flag_duplicate_name():
    token = create_user_and_login(client)
    client.post("/flags",
                json={"name": "flag1", "value": True, "description": "d1"},
                headers=auth_headers(token))
    client.post("/flags",
                json={"name": "flag2", "value": False, "description": "d2"}, 
                headers=auth_headers(token))

    # tenta renomear flag1 para flag2 → erro
    res = client.put("/flags/flag1", json={
        "name": "flag2",
        "description": "new desc"
    }, headers=auth_headers(token))

    assert res.status_code == 500


def test_delete_flag_success():
    token = create_user_and_login(client)
    client.post("/flags", json={"name": "todelete", "value": False, "description": ""}, headers=auth_headers(token))
    
    res = client.delete("/flags/todelete", headers=auth_headers(token))
    assert res.status_code == 200

    # tentar pegar → 404
    res2 = client.get("/flags/todelete")
    assert res2.status_code == 404


def test_delete_flag_not_found():
    token = create_user_and_login(client)
    res = client.delete("/flags/notexists", headers=auth_headers(token))
    assert res.status_code == 404

# ============================================================
# TESTES DE USERS
# ============================================================

def test_create_user_success():
    response = client.post("/users", json={
        "name": "John Doe",
        "email": "john@example.com",
        "password": "randompassword123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "john@example.com"
    assert data["name"] == "John Doe"
    assert data["password"] != "randomedpassword123"


def test_create_user_duplicate_email():
    # cria o primeiro
    client.post("/users", json={
        "name": "John Doe",
        "email": "john@example.com",
        "password": "random"
    })

    # tenta duplicar email
    response = client.post("/users", json={
        "name": "John X",
        "email": "john@example.com",
        "password": "random2"
    })

    assert response.status_code == 500      # DUPLICATE
    assert "already exists" in response.json()["detail"]


def test_list_users():
    client.post("/users", json={
        "name": "A",
        "email": "a@a.com",
        "password": "p1"
    })

    client.post("/users", json={
        "name": "B",
        "email": "b@b.com",
        "password": "p2"
    })

    response = client.get("/users")
    assert response.status_code == 200

    users = response.json()
    assert len(users) == 2

    emails = [u["email"] for u in users]
    assert "a@a.com" in emails
    assert "b@b.com" in emails


def test_get_user_success():
    # cria o user
    create_res = client.post("/users", json={
        "name": "Tester",
        "email": "tester@example.com",
        "password": "pass"
    })
    assert create_res.status_code == 201

    # pega o ID retornado da tabela
    list_res = client.get("/users")
    user_id = list_res.json()[0]["id"]

    # consultar
    res = client.get(f"/users/{user_id}")
    assert res.status_code == 200
    user = res.json()

    assert user["email"] == "tester@example.com"
    assert user["name"] == "Tester"
    assert "createdAt" in user


def test_get_user_not_found():
    res = client.get("/users/9999")
    assert res.status_code == 404


def test_update_user_success():
    token = create_user_and_login(client)
    # cria
    client.post("/users", json={
        "name": "Old",
        "email": "old@mail.com",
        "password": "oldpass"
    })

    users = client.get("/users").json()
    user_id = users[0]["id"]

    # update
    res = client.put(f"/users/{user_id}", json={
        "name": "New Name",
        "email": "new@mail.com",
        "password": "newpass"
    }, headers=auth_headers(token))

    assert res.status_code == 200

    # confirmar
    res2 = client.get(f"/users/{user_id}")
    assert res2.status_code == 200
    user = res2.json()

    assert user["name"] == "New Name"
    assert user["email"] == "new@mail.com"


def test_update_user_not_found():
    token = create_user_and_login(client)
    res = client.put("/users/12345", json={
        "name": "X",
        "email": "X@mail.com",
        "password": "pass"
    }, headers=auth_headers(token))
    assert res.status_code == 404


def test_update_user_duplicate_email():
    token = create_user_and_login(client)
    # cria dois usuários
    client.post("/users", json={
        "name": "A",
        "email": "a@mail.com",
        "password": "p1"
    })
    client.post("/users", json={
        "name": "B",
        "email": "b@mail.com",
        "password": "p2"
    })

    users = client.get("/users").json()
    id_a = users[0]["id"]
    id_b = users[1]["id"]

    # tenta atualizar A para email de B
    res = client.put(f"/users/{id_a}", json={
        "name": "A updated",
        "email": "b@mail.com",
        "password": "p3"
    }, headers=auth_headers(token))

    assert res.status_code == 500   # duplicate


def test_delete_user_success():
    token = create_user_and_login(client)
    client.post("/users", json={
        "name": "DeleteMe",
        "email": "del@me.com",
        "password": "pass"
    })

    users = client.get("/users").json()
    user_id = users[0]["id"]

    res = client.delete(f"/users/{user_id}", headers=auth_headers(token))
    assert res.status_code == 200

    # procurar → not found
    res2 = client.get(f"/users/{user_id}")
    assert res2.status_code == 404


def test_delete_user_not_found():
    token = create_user_and_login(client)
    res = client.delete("/users/123123", headers=auth_headers(token))
    assert res.status_code == 404

# ============================================================
# TESTES DE USERS
# ============================================================
def test_login_success():
    client.post("/users", json={
        "name": "Alice",
        "email": "alice@mail.com",
        "password": "pass123"
    })

    res = client.post("/login", json={
        "email": "alice@mail.com",
        "password": "pass123"
    })

    assert res.status_code == 200
    assert "token" in res.json()


def test_login_invalid_password():
    client.post("/users", json={
        "name": "Bob",
        "email": "bob@mail.com",
        "password": "secret123"
    })

    res = client.post("/login", json={
        "email": "bob@mail.com",
        "password": "wrong"
    })

    assert res.status_code == 401


def test_login_invalid_email():
    res = client.post("/login", json={
        "email": "ghost@mail.com",
        "password": "x"
    })

    assert res.status_code == 401


def test_me_success():
    token = create_user_and_login(client)

    res = client.get("/me", headers=auth_headers(token))
    assert res.status_code == 200
    # assert res.json()["email"] == "user@example.com"


def test_me_invalid_token():
    res = client.get("/me", headers=auth_headers("INVALID"))
    assert res.status_code == 401
