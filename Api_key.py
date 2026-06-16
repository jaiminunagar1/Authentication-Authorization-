from fastapi.security import APIKeyHeader
from fastapi import HTTPException, Depends, FastAPI, Security
import os
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn


load_dotenv()

api_key_header = APIKeyHeader(name="my_Key")
app = FastAPI(docs_url="/api/docs")

# 1. Using Depends

# def get_api_key(api_key: str = Depends(api_key_header)):
#     if api_key == os.getenv("my_Key"):
#         return api_key
#     else:
#         raise HTTPException(status_code=403, detail="Invalid API Key")
    
# class APIKeyResponse(BaseModel):
#     name: str
#     age:int

# @app.get("/protected",response_model=APIKeyResponse)
# def protected_route(api_key: str = Depends(get_api_key)):

#     response = APIKeyResponse(name="John Doe", age=30)

#     return response

# 2. Using Security Dependency

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == os.getenv("my_Key"):
        return api_key
    else:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    
class APIKeyResponse(BaseModel):
    name: str
    age:int

@app.get("/protected",response_model=APIKeyResponse)
def protected_route(api_key: str = Depends(get_api_key)):

    response = APIKeyResponse(name="John Doe", age=30)

    return response


# 3 . pass the dependency in the route decorator

# def get_api_key(api_key: str = Depends(api_key_header)):
#     if api_key == os.getenv("my_Key"):
#         return api_key
#     else:
#         raise HTTPException(status_code=403, detail="Invalid API Key")
    
# class APIKeyResponse(BaseModel):
#     name: str
#     age:int

# @app.get("/protected",response_model=APIKeyResponse, dependencies=[Depends(get_api_key)])
# def protected_route():

#     response = APIKeyResponse(name="John Doe", age=30)

#     return response

# 4. Security 

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == os.getenv("my_Key"):
        return api_key
    else:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    
class APIKeyResponse(BaseModel):
    name: str
    age:int

@app.get("/protected",response_model=APIKeyResponse, dependencies=[Depends(get_api_key)])
def protected_route():

    response = APIKeyResponse(name="John Doe", age=30)

    return response


# Rule of thumb

# Use:

# Depends() it return the value and we can use this inside the route function

# for:

# Database sessions
# Configuration
# Services
# Utility functions
# Repository classes

# Use:

# Security() it does not return the value and we cannot use this inside the route function and it is specisically designed for security related dependencies
# And we cad define a scupe for this

# for:

# API Keys
# JWT Tokens
# OAuth2
# Current User
# Roles & Permissions

# Security() is used where credentials are extracted.
# Depends() is used when attaching the dependency to the route.

# 3. Route parameter vs dependencies=[]

# Need the returned value?

# Use a route parameter:

# @app.get("/profile")
# def profile(
#     user = Depends(get_current_user)
# ):
#     return {"username": user["sub"]}

# Here:

# user

# contains the value returned by get_current_user().

# Don't need the returned value?

# Use dependencies=[]:

# @app.get(
#     "/profile",
#     dependencies=[Depends(get_current_user)]
# )
# def profile():
#     return {"message": "success"}

# FastAPI executes the dependency, but discards its return value.

# This is common when you only want to enforce authentication.


if __name__ == "__main__":

    # uvicorn.run("Api_key:app", host="0.0.0.0", port=8000,reload=True)
    uvicorn.run("Api_key:app", host="0.0.0.0", port=8000,reload=True)