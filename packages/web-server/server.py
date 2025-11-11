from db import Storage
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status

# Creates connection with storage
storage = Storage()

# Declares the REST API server.
app = FastAPI()


# Request body definitions
class FlagCreationRequest(BaseModel):
    name: str
    value: bool
    description: str


class FlagUpdateRequest(BaseModel):
    name: str
    value: bool


# Route definitions
@app.get("/flags")
def get_flags():
    """
    Returns all stored flags.
    """
    return storage.list_flags()


@app.post("/flags")
def create_flag(request: FlagCreationRequest):
    """
    Creates a new flag.
    """
    flag_name = request.name
    flag_value = request.value
    flag_description = request.description

    success = storage.insert_flag(flag_name, flag_value, flag_description)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Problem creating flag",
        )

    return request


@app.put("/flags")
def update_flag(request: FlagUpdateRequest):
    """
    Updates a given flag.
    """
    flag_name = request.name
    flag_value = request.value

    storage.update_flag(flag_name, flag_value)

    return request


@app.get("/flags/{name}")
def check_flag_status(name: str):
    """
    Returns the status of the given flag.
    """
    flag = storage.get_flag(name)
    if not flag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Requested flag not found",
        )

    return flag


@app.delete("/flags/{name}")
def remove_flag(name: str):
    """
    Removes the given flag.
    """
    storage.remove_flag(name)
