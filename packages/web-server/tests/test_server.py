import pytest
import json
import time
from fastapi.testclient import TestClient
from unittest.mock import patch

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
# CLIENT FastAPI
# ============================================================
client = TestClient(app)


# ============================================================
# TESTES DAS ROTAS E DO STORAGE
# ============================================================

def test_create_flag_success():
    response = client.post("/flags", json={
        "name": "flag1",
        "value": True,
        "description": "desc 1"
    })
    assert response.status_code == 201
    assert response.json()["name"] == "flag1"


def test_create_flag_duplicate():
    # cria a primeira
    client.post("/flags", json={
        "name": "flag1",
        "value": True,
        "description": "desc 1"
    })
    # tenta duplicar
    response = client.post("/flags", json={
        "name": "flag1",
        "value": False,
        "description": "other desc"
    })
    assert response.status_code == 500
    assert "already exists" in response.json()["detail"]


def test_list_flags():
    # insere duas flags
    client.post("/flags", json={"name": "flag1", "value": True, "description": "d1"})
    client.post("/flags", json={"name": "flag2", "value": False, "description": "d2"})

    res = client.get("/flags")
    assert res.status_code == 200
    flags = res.json()
    assert len(flags) == 2
    assert flags[0]["name"] in ["flag1", "flag2"]
    assert flags[1]["name"] in ["flag1", "flag2"]


def test_get_flag_and_log_usage():
    client.post("/flags", json={"name": "flagX", "value": True, "description": "test log"})

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
    client.post("/flags", json={"name": "flagY", "value": True, "description": ""})

    res = client.put("/flags/flagY/toggle")
    assert res.status_code == 200
    assert res.json()["new_value"] is False

    res = client.put("/flags/flagY/toggle")
    assert res.json()["new_value"] is True


def test_toggle_not_found():
    res = client.put("/flags/noFlag/toggle")
    assert res.status_code == 404


def test_update_flag_success():
    client.post("/flags",
                json={"name": "oldName", "value": True, "description": "old"})

    res = client.put("/flags/oldName", json={
        "name": "newName",
        "description": "updated description"
    })

    assert res.status_code == 200

    # checar se atualizou mesmo
    get_res = client.get("/flags/newName")
    assert get_res.status_code == 200
    flag = get_res.json()
    assert flag["name"] == "newName"
    assert flag["description"] == "updated description"


def test_update_flag_not_found():
    res = client.put("/flags/ghost", json={
        "name": "anything",
        "description": "..."
    })
    assert res.status_code == 404


def test_update_flag_duplicate_name():
    client.post("/flags",
                json={"name": "flag1", "value": True, "description": "d1"})
    client.post("/flags",
                json={"name": "flag2", "value": False, "description": "d2"})

    # tenta renomear flag1 para flag2 → erro
    res = client.put("/flags/flag1", json={
        "name": "flag2",
        "description": "new desc"
    })

    assert res.status_code == 500


def test_delete_flag_success():
    client.post("/flags", json={"name": "todelete", "value": False, "description": ""})
    
    res = client.delete("/flags/todelete")
    assert res.status_code == 200

    # tentar pegar → 404
    res2 = client.get("/flags/todelete")
    assert res2.status_code == 404


def test_delete_flag_not_found():
    res = client.delete("/flags/notexists")
    assert res.status_code == 404
