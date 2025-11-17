import pytest
import json
import time
import uuid
from fastapi.testclient import TestClient

from db import Storage
from server import app


# ============================================================
# FIXTURE: banco em memória
# ============================================================
@pytest.fixture(autouse=True)
def mock_storage(monkeypatch):
    """
    Substitui o storage real por um banco SQLite em memória.
    Também recria o usuário admin.
    """
    test_storage = Storage(":memory:")
    test_storage._create_table()

    # cria admin inicial
    test_storage.create_user("Administrator", "admin@admin.com", "admin")

    monkeypatch.setattr("server.storage", test_storage)

    return test_storage


client = TestClient(app)


# ============================================================
# HELPERS
# ============================================================
def create_user_and_login(client, name="User"):
    email = f"user_{uuid.uuid4()}@mail.com"
    password = "test12345"

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

    return token, email


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


# ============================================================
# TESTES DE FLAGS
# ============================================================
def test_create_flag_success():
    token, _ = create_user_and_login(client)

    res = client.post("/flags", json={
        "name": "flag1",
        "value": True,
        "description": "desc"
    }, headers=auth_headers(token))

    assert res.status_code == 201
    assert res.json()["name"] == "flag1"


def test_create_flag_duplicate():
    token, _ = create_user_and_login(client)

    client.post("/flags", json={
        "name": "flag1",
        "value": True,
        "description": "d1"
    }, headers=auth_headers(token))

    res = client.post("/flags", json={
        "name": "flag1",
        "value": False,
        "description": "duplicated"
    }, headers=auth_headers(token))

    assert res.status_code == 500
    assert "already exists" in res.json()["detail"]


def test_list_flags():
    token, _ = create_user_and_login(client)

    client.post("/flags", json={"name": "f1", "value": True, "description": ""}, headers=auth_headers(token))
    client.post("/flags", json={"name": "f2", "value": False, "description": ""}, headers=auth_headers(token))

    res = client.get("/flags")
    assert res.status_code == 200

    names = {f["name"] for f in res.json()}
    assert names == {"f1", "f2"}


def test_get_flag_and_log_usage():
    token, _ = create_user_and_login(client)

    client.post("/flags", json={"name": "flagX", "value": True, "description": ""}, headers=auth_headers(token))

    res1 = client.get("/flags/flagX")
    assert res1.status_code == 200

    body1 = res1.json()
    assert len(body1["usage_log"]) == 1

    res2 = client.get("/flags/flagX")
    body2 = res2.json()
    assert len(body2["usage_log"]) == 2


def test_get_flag_not_found():
    res = client.get("/flags/nope")
    assert res.status_code == 404


def test_toggle_flag():
    token, _ = create_user_and_login(client)
    client.post("/flags", json={"name": "TFLAG", "value": True, "description": ""}, headers=auth_headers(token))

    r1 = client.put("/flags/TFLAG/toggle", headers=auth_headers(token))
    assert r1.status_code == 200
    assert r1.json()["new_value"] is False

    r2 = client.put("/flags/TFLAG/toggle", headers=auth_headers(token))
    assert r2.json()["new_value"] is True


def test_toggle_not_found():
    token, _ = create_user_and_login(client)
    res = client.put("/flags/ghost/toggle", headers=auth_headers(token))
    assert res.status_code == 404


def test_update_flag_success():
    token, _ = create_user_and_login(client)

    client.post("/flags", json={"name": "old", "value": True, "description": "x"}, headers=auth_headers(token))

    res = client.put("/flags/old", json={
        "name": "newname",
        "description": "updated"
    }, headers=auth_headers(token))

    assert res.status_code == 200

    res2 = client.get("/flags/newname")
    assert res2.status_code == 200
    assert res2.json()["description"] == "updated"


def test_update_flag_not_found():
    token, _ = create_user_and_login(client)
    res = client.put("/flags/notfound", json={
        "name": "x",
        "description": "y"
    }, headers=auth_headers(token))

    assert res.status_code == 404


def test_update_flag_duplicate_name():
    token, _ = create_user_and_login(client)

    client.post("/flags", json={"name": "A", "value": True, "description": ""}, headers=auth_headers(token))
    client.post("/flags", json={"name": "B", "value": False, "description": ""}, headers=auth_headers(token))

    res = client.put("/flags/A", json={
        "name": "B",
        "description": "test"
    }, headers=auth_headers(token))

    assert res.status_code == 500


def test_delete_flag_success():
    token, _ = create_user_and_login(client)

    client.post("/flags", json={"name": "deleteMe", "value": False, "description": ""}, headers=auth_headers(token))

    res = client.delete("/flags/deleteMe", headers=auth_headers(token))
    assert res.status_code == 200

    res2 = client.get("/flags/deleteMe")
    assert res2.status_code == 404


def test_delete_flag_not_found():
    token, _ = create_user_and_login(client)
    res = client.delete("/flags/none", headers=auth_headers(token))
    assert res.status_code == 404


# ============================================================
# TESTES DE USUÁRIOS
# ============================================================
def test_create_user_success():
    res = client.post("/users", json={
        "name": "John",
        "email": "john@mail.com",
        "password": "pass"
    })
    assert res.status_code == 201
    assert res.json()["email"] == "john@mail.com"


def test_create_user_duplicate_email():
    client.post("/users", json={
        "name": "Test",
        "email": "a@mail.com",
        "password": "pass"
    })

    res = client.post("/users", json={
        "name": "Other",
        "email": "a@mail.com",
        "password": "pass2"
    })

    assert res.status_code == 500


def test_list_users():
    client.post("/users", json={"name": "A", "email": "a@a.com", "password": "x"})
    client.post("/users", json={"name": "B", "email": "b@b.com", "password": "x"})

    res = client.get("/users")
    assert res.status_code == 200

    emails = {u["email"] for u in res.json()}
    assert "a@a.com" in emails
    assert "b@b.com" in emails


def test_get_user_success():
    create = client.post("/users", json={
        "name": "Z",
        "email": "z@mail.com",
        "password": "x"
    })

    user_id = client.get("/users").json()[-1]["id"]

    res = client.get(f"/users/{user_id}")
    assert res.status_code == 200
    assert res.json()["email"] == "z@mail.com"


def test_get_user_not_found():
    res = client.get("/users/9999")
    assert res.status_code == 404


def test_update_user_success():
    token, _ = create_user_and_login(client)

    client.post("/users", json={
        "name": "Old",
        "email": "old@mail.com",
        "password": "123"
    })

    user_id = client.get("/users").json()[-1]["id"]

    res = client.put(f"/users/{user_id}", json={
        "name": "New",
        "email": "new@mail.com",
        "password": "abc"
    }, headers=auth_headers(token))

    assert res.status_code == 200

    updated = client.get(f"/users/{user_id}").json()
    assert updated["email"] == "new@mail.com"


def test_update_user_not_found():
    token, _ = create_user_and_login(client)

    res = client.put("/users/9999", json={
        "name": "X",
        "email": "x@mail.com",
        "password": "x"
    }, headers=auth_headers(token))

    assert res.status_code == 404


def test_update_user_duplicate_email():
    token, _ = create_user_and_login(client)

    client.post("/users", json={"name": "A", "email": "a@mail.com", "password": "1"})
    client.post("/users", json={"name": "B", "email": "b@mail.com", "password": "1"})

    users = client.get("/users").json()
    id_a = users[-2]["id"]
    id_b = users[-1]["id"]

    res = client.put(f"/users/{id_a}", json={
        "name": "A2",
        "email": "b@mail.com",
        "password": "new"
    }, headers=auth_headers(token))

    assert res.status_code == 500


def test_delete_user_success():
    token, _ = create_user_and_login(client)

    client.post("/users", json={"name": "X", "email": "x@mail.com", "password": "x"})
    user_id = client.get("/users").json()[-1]["id"]

    res = client.delete(f"/users/{user_id}", headers=auth_headers(token))
    assert res.status_code == 200

    res2 = client.get(f"/users/{user_id}")
    assert res2.status_code == 404


def test_delete_user_not_found():
    token, _ = create_user_and_login(client)

    res = client.delete("/users/8888", headers=auth_headers(token))
    assert res.status_code == 404


# ============================================================
# TESTES LOGIN
# ============================================================
def test_login_success():
    client.post("/users", json={
        "name": "Alice",
        "email": "alice@mail.com",
        "password": "pass"
    })
    res = client.post("/login", json={"email": "alice@mail.com", "password": "pass"})

    assert res.status_code == 200
    assert "token" in res.json()


def test_login_invalid_password():
    client.post("/users", json={
        "name": "Bob",
        "email": "bob@mail.com",
        "password": "secret"
    })
    res = client.post("/login", json={"email": "bob@mail.com", "password": "wrong"})
    assert res.status_code == 401


def test_login_invalid_email():
    res = client.post("/login", json={"email": "ghost@mail.com", "password": "x"})
    assert res.status_code == 401


def test_me_success():
    token, email = create_user_and_login(client)

    res = client.get("/me", headers=auth_headers(token))
    assert res.status_code == 200
    assert "email" in res.json()


def test_me_invalid_token():
    res = client.get("/me", headers=auth_headers("INVALID"))
    assert res.status_code == 401
