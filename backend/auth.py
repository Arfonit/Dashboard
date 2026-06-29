from jose import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

auth = HTTPBearer()

SECRET = "secret_key"
ALGO = "HS256"

def create_token(user: str):
    payload = {
        "sub": user,
        "exp": datetime.utcnow() + timedelta(hours=6)
    }
    return jwt.encode(payload, SECRET, algorithm=ALGO)

def verify(token=Depends(auth)):
    try:
        jwt.decode(token.credentials, SECRET, algorithms=[ALGO])
    except:
        raise HTTPException(401, "Invalid token")
    
@app.get("/dashboard")
async def dashboard(user=Depends(verify)):
    ...