from unittest.mock import Mock
from src.openflag import OpenFlag


def test_login_correct_credentials():
    openflag = OpenFlag()
    openflag._conn.post = Mock(return_value=(200, {"token": "abc"}))

    result = openflag.login(email="mock@mock.com", password="123")

    assert result == 0
    assert openflag._headers["Authorization"] == "Bearer abc"


def test_login_incorrect_credentials():
    openflag = OpenFlag()
    openflag._conn.post = Mock(return_value=(401, {}))

    result = openflag.login(email="mock@mock.com", password="123")

    assert result == -4
    assert openflag._headers["Authorization"] == ""


def test_login_correct_credentials():
    openflag = OpenFlag()
    openflag._conn.post = Mock(return_value=(200, {"token": "abc"}))

    result = openflag.login(email="mock@mock.com", password="123")

    assert result == 0
    assert openflag._headers["Authorization"] == "Bearer abc"


def test_get_user_id_not_logged():
    openflag = OpenFlag()
    openflag._conn.get = Mock(return_value=(401, {}))

    result = openflag.get_user_id()

    assert result == -4


def test_get_user_id_logged():
    openflag = OpenFlag()
    openflag._conn.get = Mock(return_value=(200, {"user_id": "4"}))

    result = openflag.get_user_id()

    assert result == 4


def test_list_users():
    openflag = OpenFlag()
    openflag._conn.get = Mock(return_value=(200, ["User A", "User B"]))

    users = openflag.list_users()

    assert isinstance(users, list)


def test_create_new_user():
    openflag = OpenFlag()
    openflag._conn.post = Mock(return_value=(201, {}))

    result = openflag.create_user("New User", "user@email.com", "password123")

    assert result == 0


def test_create_existent_user():
    openflag = OpenFlag()
    openflag._conn.post = Mock(return_value=(500, {}))

    result = openflag.create_user("Existent User", "user@email.com", "password123")

    assert result == -2


def test_create_new_user_not_logged():
    openflag = OpenFlag()
    openflag._conn.post = Mock(return_value=(401, {}))

    result = openflag.create_user("New User", "user@email.com", "password123")

    assert result == -4


def test_check_existent_user():
    openflag = OpenFlag()
    openflag._conn.get = Mock(
        return_value=(
            200,
            {
                "id": 1,
                "name": "admin",
                "email": "admin@email.com",
                "password": "123",
                "createdAt": 1763304431.887579,
            },
        )
    )

    result = openflag.check_user("admin")

    assert isinstance(result, dict)
    assert result["name"] == "admin"


def test_check_nonexistent_user():
    openflag = OpenFlag()
    openflag._conn.get = Mock(return_value=(404, {}))

    result = openflag.check_flag("Non-existent User")

    assert result == -1


def test_update_existent_user():
    openflag = OpenFlag()
    openflag._conn.put = Mock(return_value=(200, {}))

    result = openflag.update_user(1, "New Name", "New Email", "New Password")

    assert result == 0


def test_update_nonexistent_user():
    openflag = OpenFlag()
    openflag._conn.put = Mock(return_value=(404, {}))

    result = openflag.update_user(2, "New Name", "New Email", "New Password")

    assert result == -1


def test_update_user_not_logged():
    openflag = OpenFlag()
    openflag._conn.put = Mock(return_value=(401, {}))

    result = openflag.update_user(3, "Name", "Email", "Password")

    assert result == -4


def test_remove_existent_user():
    openflag = OpenFlag()
    openflag._conn.delete = Mock(return_value=(200, {}))

    result = openflag.remove_user(1)

    assert result == 0


def test_remove_nonexistent_user():
    openflag = OpenFlag()
    openflag._conn.delete = Mock(return_value=(404, {}))

    result = openflag.remove_user(2)

    assert result == -1


def test_remove_user_not_logged():
    openflag = OpenFlag()
    openflag._conn.delete = Mock(return_value=(401, {}))

    result = openflag.remove_user(3)

    assert result == -4


def test_list_flags():
    openflag = OpenFlag()
    openflag._conn.get = Mock(return_value=(200, ["Flag A", "Flag B"]))

    flags = openflag.list_flags()

    assert isinstance(flags, list)


def test_create_new_flag():
    openflag = OpenFlag()
    openflag._conn.post = Mock(return_value=(201, {}))

    result = openflag.create_flag("New Flag", True, "This is a test flag.")

    assert result == 0


def test_create_existent_flag():
    openflag = OpenFlag()
    openflag._conn.post = Mock(return_value=(500, {}))

    result = openflag.create_flag(
        "Existent Flag", True, "This is an existing test flag."
    )

    assert result == -2


def test_create_new_flag_not_logged():
    openflag = OpenFlag()
    openflag._conn.post = Mock(return_value=(401, {}))

    result = openflag.create_flag("New Flag", True, "This is a test flag.")

    assert result == -4


def test_update_existent_flag():
    openflag = OpenFlag()
    openflag._conn.put = Mock(return_value=(200, {}))

    result = openflag.update_flag("Existent Flag", "New Name", "New Description")

    assert result == 0


def test_update_nonexistent_flag():
    openflag = OpenFlag()
    openflag._conn.put = Mock(return_value=(404, {}))

    result = openflag.update_flag("Non-existent Flag", "New Name", "New Description.")

    assert result == -1


def test_update_flag_not_logged():
    openflag = OpenFlag()
    openflag._conn.put = Mock(return_value=(401, {}))

    result = openflag.update_flag("Flag", "Name", "Description")

    assert result == -4


def test_toggle_existent_flag():
    openflag = OpenFlag()
    openflag._conn.put = Mock(return_value=(200, {}))

    result = openflag.toggle_flag("Existent Flag")

    assert result == 0


def test_toggle_nonexistent_flag():
    openflag = OpenFlag()
    openflag._conn.put = Mock(return_value=(404, {}))

    result = openflag.toggle_flag("Non-existent Flag")

    assert result == -1


def test_toggle_flag_not_logged():
    openflag = OpenFlag()
    openflag._conn.put = Mock(return_value=(401, {}))

    result = openflag.toggle_flag("Flag")

    assert result == -4


def test_check_existent_flag():
    openflag = OpenFlag()
    openflag._conn.get = Mock(
        return_value=(
            200,
            {
                "name": "Existent Flag",
                "value": True,
                "description": "Flag",
                "usage_log": [1763307897.7247112],
            },
        )
    )

    result = openflag.check_flag("Existent Flag")

    assert isinstance(result, dict)
    assert result["name"] == "Existent Flag"


def test_check_nonexistent_flag():
    openflag = OpenFlag()
    openflag._conn.get = Mock(return_value=(404, {}))

    result = openflag.check_flag("Non-existent Flag")

    assert result == -1


def test_remove_existent_flag():
    openflag = OpenFlag()
    openflag._conn.delete = Mock(return_value=(200, {}))

    result = openflag.remove_flag("Existent Flag")

    assert result == 0


def test_remove_nonexistent_flag():
    openflag = OpenFlag()
    openflag._conn.delete = Mock(return_value=(404, {}))

    result = openflag.remove_flag("Non-existent Flag")

    assert result == -1


def test_remove_flag_not_logged():
    openflag = OpenFlag()
    openflag._conn.delete = Mock(return_value=(401, {}))

    result = openflag.remove_flag("Flag")

    assert result == -4
