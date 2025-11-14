import requests


class OpenFlag:
    def __init__(self, host: str = "localhost", port: int = 8000):
        self.host = host
        self.port = str(port)

    def list(self):
        """
        Returns a list of all flags stored in the system.

        Returns:
        list(str): List with names of stored flags
        -3 (int): Unknown error
        """
        response = requests.get(f"http://{self.host}:{self.port}/flags")
        flag_list = response.json()

        # Captures any errors
        if response.status_code != 200:
            return -3
        if not isinstance(flag_list, list):
            return -3

        return response.json()

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
        response = requests.post(f"http://{self.host}:{self.port}/flags", json=body)

        # Captures any errors
        if response.status_code == 500:
            return -2
        if response.status_code != 201:
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
        response = requests.put(
            f"http://{self.host}:{self.port}/flags/{name}", json=body
        )

        # Captures any errors
        if response.status_code == 404:
            return -1
        if response.status_code != 200:
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
        response = requests.put(f"http://{self.host}:{self.port}/flags/{name}/toggle")

        # Captures any errors
        if response.status_code == 404:
            return -1
        if response.status_code != 200:
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
        response = requests.get(f"http://{self.host}:{self.port}/flags/{name}")

        # Captures any errors
        if response.status_code == 404:
            return -1
        if response.status_code != 200:
            return -3

        # Formats the response
        raw = response.json()
        formatted = {}
        formatted["name"] = raw[0]
        formatted["value"] = raw[1]
        formatted["description"] = raw[2]
        formatted["usage_log"] = raw[3]

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
        response = requests.delete(f"http://{self.host}:{self.port}/flags/{name}")

        # Captures any errors
        if response.status_code == 404:
            return -1
        if response.status_code != 200:
            return -3

        return 0
