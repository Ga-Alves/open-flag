import requests


class OpenFlagConnection:
    """
    Wrapper around the requests library.
    Establishes a connection with the OpenFlag server.
    """

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = str(port)

        self.path = f"http://{self.host}:{self.port}/"

    def get(self, route: str):
        response = requests.get(f"{self.path}{route}")
        code, body = response.status_code, response.json()
        return code, body

    def post(self, route: str, body: dict = {}):
        response = requests.post(f"{self.path}{route}", json=body)
        code, body = response.status_code, response.json()
        return code, body

    def put(self, route: str, body: dict = {}):
        response = requests.put(f"{self.path}{route}", json=body)
        code, body = response.status_code, response.json()
        return code, body

    def delete(self, route: str):
        response = requests.delete(f"{self.path}{route}")
        code, body = response.status_code, response.json()
        return code, body


class OpenFlag:
    """
    SDK for the OpenFlag flag management application.
    """

    def __init__(self, host: str = "localhost", port: int = 8000):
        self._conn = OpenFlagConnection(host, port)

    def list(self):
        """
        Returns a list of all flags stored in the system.

        Returns:
        list(str): List with names of stored flags
        -3 (int): Unknown error
        """
        code, response = self._conn.get("flags")

        # Captures any errors
        if code != 200:
            return -3
        if not isinstance(response, list):
            return -3

        return response

    def create(self, name: str, value: bool, description: str):
        """
        Creates a new flag.

        - name (str): The name of the flag
        - value (bool): The initial value of the flag
        - description (str): The description of the flag

        Returns:
        0 (int): Success
        -2 (int): Flag already exists
        -3 (int): Unknown error
        """
        body = {"name": name, "value": value, "description": description}
        code, response = self._conn.post("flags", body)

        # Captures any errors
        if code == 500:
            return -2
        if code != 201:
            return -3

        return 0

    def update(self, name: str, new_name: str, new_description: str):
        """
        Updates the name and/or description of the given flag.

        - name (str): The name of the flag to be modified
        - new_name (str): The new desired name
        - new_description (str): The new desired description

        Returns:
        0 (int): Success
        -1 (int): Flag not found
        -3 (int): Unknown error
        """
        body = {"name": new_name, "description": new_description}
        code, response = self._conn.put(f"flags/{name}", body=body)

        # Captures any errors
        if code == 404:
            return -1
        if code != 200:
            return -3

        return 0

    def toggle(self, name: str):
        """
        Toggles the value (on/off) of the given flag.

        - name (str): The name of the flag to be toggled

        Returns:
        0 (int): Success
        -1 (int): Flag not found
        -3 (int): Unknown error
        """
        code, response = self._conn.put(f"flags/{name}/toggle")

        # Captures any errors
        if code == 404:
            return -1
        if code != 200:
            return -3

        return 0

    def check(self, name: str):
        """
        Returns the current value of the given flag.

        - name (str): The name of the flag to be checked

        Returns:
        (bool): The value of the flag
        -1 (int): Flag not found
        -3 (int): Unknown error
        """
        code, response = self._conn.get(f"flags/{name}")

        # Captures any errors
        if code == 404:
            return -1
        if code != 200:
            return -3

        # Formats the response
        formatted = {}
        formatted["name"] = response[0]
        formatted["value"] = response[1]
        formatted["description"] = response[2]
        formatted["usage_log"] = response[3]

        return formatted

    def remove(self, name: str):
        """
        Excludes the given flag.

        - name (str): The name of the flag to be excluded

        Returns:
        0 (int): Success
        -1 (int): Flag not found
        -3 (int): Unknown error
        """
        code, response = self._conn.delete(f"flags/{name}")

        # Captures any errors
        if code == 404:
            return -1
        if code != 200:
            return -3

        return 0
