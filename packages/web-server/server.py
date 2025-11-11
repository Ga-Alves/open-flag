from db import Storage
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status

# Creates connection with storage
storage = Storage()

# Error handling
error_codes = {
    0: (status.HTTP_200_OK, "Operation successfull!"),
    -1: (status.HTTP_404_NOT_FOUND, f"Flag with ID {ID} not found!"),
    -2: (status.HTTP_500_INTERNAL_SERVER_ERROR, f"Flag with ID {ID} already exists!"),
}

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
    code, res = storage.list_flags()

    return res


@app.post("/flags", status_code=status.HTTP_201_CREATED)
def create_flag(request: FlagCreationRequest):
    """
    Creates a new flag.
    """
    flag_name = request.name
    flag_value = request.value
    flag_description = request.description

    code, res = storage.insert_flag(flag_name, flag_value, flag_description)

    if code != 0:
        error = error_codes[code]
        raise HTTPException(
            status_code=error[0],
            detail=error[1],
        )

    return request


@app.put("/flags", status_code=status.HTTP_200_OK)
def update_flag(request: FlagUpdateRequest):
    """
    Updates a given flag.
    """
    flag_name = request.name
    flag_value = request.value

    code, res = storage.update_flag(flag_name, flag_value)

    if code != 0:
        error = error_codes[code]
        raise HTTPException(
            status_code=error[0],
            detail=error[1],
        )

    return request


@app.get("/flags/{name}", status_code=status.HTTP_200_OK)
def check_flag_status(name: str):
    """
    Returns the status of the given flag.
    """
    code, res = storage.get_flag(name)

    if code != 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Requested flag not found",
        )

    return res


@app.delete("/flags/{name}", status_code=status.HTTP_200_OK)
def remove_flag(name: str):
    """
    Removes the given flag.
    """
    code, res = storage.remove_flag(name)

    if code != 0:
        error = error_codes[code]
        raise HTTPException(
            status_code=error[0],
            detail=error[1],
        )

    return name
