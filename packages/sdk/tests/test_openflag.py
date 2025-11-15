from unittest.mock import Mock
from src.openflag import OpenFlag


def test_list_flags():
    openflag = OpenFlag()
    openflag._conn.get = Mock(return_value=(200, ["Flag A", "Flag B"]))

    flags = openflag.list()

    assert isinstance(flags, list)


def test_create_new_flag():
    openflag = OpenFlag()
    openflag._conn.post = Mock(return_value=(201, {}))

    result = openflag.create("New Flag", True, "This is a test flag.")

    assert result == 0


def test_create_existent_flag():
    openflag = OpenFlag()
    openflag._conn.post = Mock(return_value=(500, {}))

    result = openflag.create("Existent Flag", True, "This is an existing test flag.")

    assert result == -2


def test_update_existent_flag():
    openflag = OpenFlag()
    openflag._conn.put = Mock(return_value=(200, {}))

    result = openflag.update("Existent Flag", "New Name", "New Description")

    assert result == 0


def test_update_nonexistent_flag():
    openflag = OpenFlag()
    openflag._conn.put = Mock(return_value=(404, {}))

    result = openflag.update("Non-existent Flag", "New Name", "New Description.")

    assert result == -1


def test_toggle_existent_flag():
    openflag = OpenFlag()
    openflag._conn.put = Mock(return_value=(200, {}))

    result = openflag.toggle("Existent Flag")

    assert result == 0


def test_toggle_nonexistent_flag():
    openflag = OpenFlag()
    openflag._conn.put = Mock(return_value=(404, {}))

    result = openflag.toggle("Non-existent Flag")

    assert result == -1


def test_check_existent_flag():
    openflag = OpenFlag()
    openflag._conn.get = Mock(
        return_value=(200, ["Existent Flag", True, "Lorem Ipsum", [0.0, 1.0]])
    )

    result = openflag.check("Existent Flag")

    assert isinstance(result, dict)
    assert result["name"] == "Existent Flag"


def test_check_nonexistent_flag():
    openflag = OpenFlag()
    openflag._conn.get = Mock(return_value=(404, {}))

    result = openflag.check("Non-existent Flag")

    assert result == -1


def test_remove_existent_flag():
    openflag = OpenFlag()
    openflag._conn.delete = Mock(return_value=(200, {}))

    result = openflag.remove("Existent Flag")

    assert result == 0


def test_remove_nonexistent_flag():
    openflag = OpenFlag()
    openflag._conn.delete = Mock(return_value=(404, {}))

    result = openflag.remove("Non-existent Flag")

    assert result == -1
