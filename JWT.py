from jose import jwt,JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, FastAPI,Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import uvicorn

from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")



def create_access_token(payload: dict, secret_key: str, algorithm: str):

    to_encode = payload.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})

    print ("Payload to encode:", to_encode)

    return jwt.encode(to_encode, secret_key, algorithm=algorithm)



class LoginRequest(BaseModel):
    username: str
    password: str
class TokenResponse(BaseModel):
    access_token: str
    token_type: str


app = FastAPI(docs_url="/api/docs")

@app.post("/login" , response_model = TokenResponse)
async def login(request: LoginRequest):

    payload_username = request.username
    payload_password = request.password

    if payload_username == "admin" and payload_password == "Admin@123":
        payload = {"sub": payload_username}
        token = create_access_token(payload, SECRET_KEY, ALGORITHM)
        return TokenResponse(access_token=token, token_type="bearer")
    raise HTTPException(status_code=401, detail="Invalid credentials")


security = HTTPBearer()

def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):  
    schema = credentials.scheme
    token = credentials.credentials
    print(f"Received token: {token}and schema: {schema}")

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    

@app.get("/employees")
def get_employees(
    user=Depends(verify_token)
):
    return {
        "message": "Authorized",
        "user": user
    }

if __name__ == "__main__":

    uvicorn.run("JWT:app", host="0.0.0.0", port=8000,reload=True)

    # payload = {"sub": "admin"}

    # token = create_access_token(payload, SECRET_KEY, ALGORITHM)
    # print("Generated JWT:", token)