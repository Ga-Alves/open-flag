import requests


class OpenFlag:
    def __init__(self, host: str = "localhost", port: int = 8000):
        self.host = host
        self.port = str(port)

    def list(self):
        response = requests.get(f"http://{self.host}:{self.port}/flags")
        response = response.json()
        return response

    def create(self, name: str, value):
        body = {"name": name, "value": str(value)}
        response = requests.post(f"http://{self.host}:{self.port}/flags", json=body)
        response = response.json()
        return response

    def update(self, name: str, value):
        body = {"name": name, "value": str(value)}
        response = requests.put(f"http://{self.host}:{self.port}/flags", json=body)
        response = response.json()
        return response

    def check(self, name: str):
        response = requests.get(f"http://{self.host}:{self.port}/flags/{name}/check")
        response = response.json()
        return eval(response)

    def remove(self, name: str):
        response = requests.delete(f"http://{self.host}:{self.port}/flags/{name}/check")
        response = response.json()
        return eval(response)
