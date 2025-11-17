from datetime import datetime
import json
from db import Storage
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status, Depends, Header, APIRouter
from fastapi.middleware.cors import CORSMiddleware 

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body definitions
class FlagCreationRequest(BaseModel):
    name: str
    value: bool
    description: str

class FlagUpdateRequest(BaseModel):
    name: str
    description: str

class UserCreateRequest(BaseModel):
    name: str
    email: str
    password: str

class UserUpdateRequest(BaseModel):
    name: str
    email: str
    password: str | None = None


# ============================ PRE HANDLER ============================
def auth_required(authorization: str = Header(None)):
    """
    Dependency que valida o JWT. 
    Roda antes da rota (pre-handler).
    """
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header"
        )

    token = authorization.replace("Bearer ", "")

    try:
        payload = storage.validate_token(token)
        return payload  # Pode ser usado dentro da rota se quiser
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

# protected = APIRouter(prefix="", dependencies=[Depends(auth_required)])
# app.include_router(protected)

# ============================ USER ROUTES ============================

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
            "usage_timestamps": json.loads( flag["usage_log"]),
        }
        formatted_flags.append(flag_data)
    
    return formatted_flags

@app.post("/flags", status_code=status.HTTP_201_CREATED, dependencies=[Depends(auth_required)])
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

@app.put("/flags/{name}", status_code=status.HTTP_200_OK, dependencies=[Depends(auth_required)])
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

@app.put("/flags/{name}/toggle", status_code=status.HTTP_200_OK, dependencies=[Depends(auth_required)])
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

@app.delete("/flags/{name}", status_code=status.HTTP_200_OK, dependencies=[Depends(auth_required)])
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

# ============================ USER ROUTES ============================

@app.get("/users", status_code=status.HTTP_200_OK)
def list_users():
    code, users = storage.list_users()

    if code != 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error listing users"
        )

    return users


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(request: UserCreateRequest):
    code, _ = storage.create_user(
        name=request.name,
        email=request.email,
        password=request.password
    )

    if code != 0:
        error = error_codes[code]
        raise HTTPException(status_code=error[0], detail=error[1])

    return request


@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int):
    code, user = storage.get_user(user_id=user_id)

    if code != 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!"
        )

    return user


@app.put("/users/{user_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(auth_required)])
def update_user(user_id: int, request: UserUpdateRequest):
    code, _ = storage.update_user(
        user_id=user_id,
        name=request.name,
        email=request.email,
        password=request.password
    )

    if code != 0:
        error = error_codes[code]
        raise HTTPException(status_code=error[0], detail=error[1])

    return request


@app.delete("/users/{user_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(auth_required)])
def delete_user(user_id: int):
    code, _ = storage.delete_user(user_id)

    if code != 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!"
        )

    return {"message": f"User {user_id} deleted successfully"}

# ===================== AUTH ROUTES =======================

@app.post("/login")
def login(data: dict):
    try:
        token = storage.login(data["email"], data["password"])
        return {"token": token}
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    

@app.get("/me")
def get_me(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    print(token)
    try:
        payload = storage.validate_token(token)
        return {"user_id": payload["sub"], "email": payload["email"]}
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token")