from fastapi import FastAPI
from pydantic import BaseModel

# Temporary storage mechanism
storage = {}

# Declares the REST API server.
app = FastAPI()


# Request body definitions
class FlagCreationRequest(BaseModel):
    name: str
    value: str


class FlagUpdateRequest(BaseModel):
    name: str
    value: str


# Route definitions
@app.get("/flags")
def get_flags():
    """
    Returns all stored flags.
    """
    return list(storage.keys())


@app.post("/flags")
def create_flag(request: FlagCreationRequest):
    """
    Creates a new flag.
    """
    flag_name = request.name
    flag_value = request.value

    storage[flag_name] = flag_value

    return request


@app.put("/flags")
def update_flag(request: FlagUpdateRequest):
    """
    Updates a given flag.
    """
    flag_name = request.name
    flag_value = request.value

    storage[flag_name] = flag_value

    return request


@app.get("/flags/{name}/check")
def check_flag_status(name: str):
    """
    Returns the status of the given flag.
    """
    return storage[name]
