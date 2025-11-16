# Open Flag — Python SDK

***Software development kit*** da plataforma **OpenFlag** para a linguagem de programação Python. Permite gerenciar feature flags, incluindo criação, edição, remoção, toggle e histórico de uso (timestamps), a nível de código.


## 🚀 Quick Start

### **Instalação**

```bash
cd dist/
pip install openflag-X.Y.Z.tar.gz
```

### **Exemplo de uso**

```python
>>> from openflag import OpenFlag

>>> conn = OpenFlag()
>>> conn.list()
[]

>>> conn.create("Flag", True, "This is an example.")
>>> conn.list()
["Flag"]

>>> conn.check("Flag")
{"name": "Flag", "value": True, "description": "This is an example.", "usage_log": [1000.0]}
```

### **Execução dos testes**

```bash
pip install -r tests/requirements.txt
pytest tests/
```

## 📁 Estrutura do projeto

```
sdk/
│── dist/            # Pacote instalável
│── src/             # Código-fonte
│── tests/           # Testes de unidade (pytest)
│── LICENSE          # Licença de uso (MIT)
│── pyproject.toml   # Configurações do projeto
│── README.md        # Esta documentação
```

## ⚙️ API Reference
    class OpenFlag()
     |  OpenFlag(host: str = 'localhost', port: int = 8000)
     |
     |  SDK for the OpenFlag flag management application.
     |
     |  ----------------------------------------------------------------------
     |
     |  check_flag(self, name: str)
     |      Returns the current value of the given flag.
     |
     |      - name (str): The name of the flag to be checked
     |
     |      Returns:
     |      (dict): The information associated with the flag
     |      -1 (int): Flag not found
     |      -3 (int): Unknown error
     |
     |  ----------------------------------------------------------------------
     |
     |  check_user(self, user_id: int)
     |      Returns the data associated with the given user.
     |
     |      - user_id (int): The ID of the user to be checked
     |
     |      Returns:
     |      (bool): The value of the flag
     |      -1 (int): User not found
     |      -3 (int): Unknown error
     |
     |  ----------------------------------------------------------------------
     |
     |  create_flag(self, name: str, value: bool, description: str)
     |      Creates a new flag.
     |
     |      - name (str): The name of the flag
     |      - value (bool): The initial value of the flag
     |      - description (str): The description of the flag
     |
     |      Returns:
     |      0 (int): Success
     |      -2 (int): Flag already exists
     |      -3 (int): Unknown error
     |      -4 (int): Unauthorized access
     |
     |  ----------------------------------------------------------------------
     |
     |  create_user(self, name: str, email: str, password: str)
     |      Creates a new user.
     |
     |      - name (str): The name of the user
     |      - email (str): The email address of the user
     |      - password (str): The password of the user
     |
     |      Returns:
     |      0 (int): Success
     |      -2 (int): User already exists
     |      -3 (int): Unknown error
     |      -4 (int): Unauthorized access
     |
     |  ----------------------------------------------------------------------
     |
     |  get_user_id(self)
     |      Returns the user ID associated with the logged account.
     |
     |      Returns:
     |      ID (int): The ID associated with the logged user
     |      -3 (int): Unknown error
     |      -4 (int): Not logged in
     |
     |  ----------------------------------------------------------------------
     |
     |  list_flags(self)
     |      Returns a list of all flags stored in the system.
     |
     |      Returns:
     |      list(str): List with names of stored flags
     |      -3 (int): Unknown error
     |
     |  ----------------------------------------------------------------------
     |
     |  list_users(self)
     |      Returns a list of all users registered in the system.
     |
     |      Returns:
     |      list(str): List with names of registered users
     |      -3 (int): Unknown error
     |
     |  ----------------------------------------------------------------------
     |
     |  login(self, email: str, password: str)
     |      Logs in to a user account.
     |
     |      - email (str): E-mail associated with the user account
     |      - password (str): Password registered for the used account
     |
     |      Returns:
     |      0 (int): Success
     |      -3 (int): Unknown error
     |      -4 (int): Invalid email or password
     |
     |  ----------------------------------------------------------------------
     |
     |  remove_flag(self, name: str)
     |      Excludes the given flag.
     |
     |      - name (str): The name of the flag to be excluded
     |
     |      Returns:
     |      0 (int): Success
     |      -1 (int): Flag not found
     |      -3 (int): Unknown error
     |      -4 (int): Unauthorized access
     |
     |  ----------------------------------------------------------------------
     |
     |  remove_user(self, user_id: int)
     |      Excludes the given user.
     |
     |      - user_id (int): The ID of the user to be excluded
     |
     |      Returns:
     |      0 (int): Success
     |      -1 (int): User not found
     |      -3 (int): Unknown error
     |      -4 (int): Unauthorized access
     |
     |  ----------------------------------------------------------------------
     |
     |  toggle_flag(self, name: str)
     |      Toggles the value (on/off) of the given flag.
     |
     |      - name (str): The name of the flag to be toggled
     |
     |      Returns:
     |      0 (int): Success
     |      -1 (int): Flag not found
     |      -3 (int): Unknown error
     |      -4 (int): Unauthorized access
     |
     |  ----------------------------------------------------------------------
     |
     |  update_flag(self, name: str, new_name: str, new_description: str)
     |      Updates the name and/or description of the given flag.
     |
     |      - name (str): The name of the flag to be modified
     |      - new_name (str): The new desired name
     |      - new_description (str): The new desired description
     |
     |      Returns:
     |      0 (int): Success
     |      -1 (int): Flag not found
     |      -3 (int): Unknown error
     |      -4 (int): Unauthorized access
     |
     |  ----------------------------------------------------------------------
     |
     |  update_user(self, user_id: int, new_name: str, new_email: str, new_password: str)
     |      Updates the attributes of the given user.
     |
     |      - user_id (int): The name of the flag to be modified
     |      - new_name (str): The new desired name
     |      - new_email (str): The new desired e-mail
     |      - new_password (str): The new desired password
     |
     |      Returns:
     |      0 (int): Success
     |      -1 (int): User not found
     |      -3 (int): Unknown error
     |      -4 (int): Unauthorized access
     |
     |  ----------------------------------------------------------------------