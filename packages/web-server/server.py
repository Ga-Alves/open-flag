from datetime import datetime
from db import Storage
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware  # ADICIONE ESTA LINHA

# Creates connection with storage
storage = Storage()

# Error handling
error_codes = {
    0: (status.HTTP_200_OK, "Operation successful!"),
    -1: (status.HTTP_404_NOT_FOUND, "Flag not found!"),
    -2: (status.HTTP_500_INTERNAL_SERVER_ERROR, "Flag already exists!"),
}

# Declares the REST API server.
app = FastAPI()

# ADICIONE ESTA CONFIGURAÇÃO CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL do seu frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos os headers
)

# Request body definitions
class FlagCreationRequest(BaseModel):
    name: str
    value: bool
    description: str

class FlagUpdateRequest(BaseModel):
    name: str
    description: str

# Route definitions
@app.get("/flags")
def get_flags():
    """
    Returns all stored flags with their usage timestamps.
    """
    _, res = storage.list_flags()
    
    # Formata a resposta para incluir informações do usage_log
    formatted_flags = []
    for flag in res:
        flag_data = {
            "name": flag["name"],
            "value": flag["value"],
            "description": flag["description"],
            "usage_timestamps": flag["usage_log"],
        }
        formatted_flags.append(flag_data)
    
    return formatted_flags

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

@app.put("/flags/{name}", status_code=status.HTTP_200_OK)
def update_flag(name:str, request: FlagUpdateRequest):
    """
    Updates a given flag.
    """
    flag_name = request.name
    flag_description = request.description

    code, res = storage.update_flag(name, flag_name, flag_description)

    if code != 0:
        error = error_codes[code]
        raise HTTPException(
            status_code=error[0],
            detail=error[1],
        )

    return request

@app.put("/flags/{name}/toggle", status_code=status.HTTP_200_OK)
def toggle_flag(name: str):
    """
    Toggles the value of a given flag (true/false).
    """
    code, res = storage.toggle_flag(name)

    if code != 0:
        error = error_codes[code]
        raise HTTPException(
            status_code=error[0],
            detail=error[1],
        )

    return {"message": f"Flag {name} toggled successfully", "new_value": res}

@app.get("/flags/{name}", status_code=status.HTTP_200_OK)
def check_flag_status(name: str):
    """
    Returns the status of the given flag.
    """
    storage.log_date_time_for_flag(name)
    
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