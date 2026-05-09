from fastapi import Header, HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

def verificar_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token não enviado")

    token = authorization.replace("Bearer ", "")

    if len(token) < 10:
        raise HTTPException(status_code=401, detail="Token inválido")

    return token

def validar_api_key(x_api_key: str = Header(None)):
    if not x_api_key:
        raise HTTPException(
            status_code=400,
            detail="Header X-API-Key é obrigatório"
        )

    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="API Key inválida"
        )

    return x_api_key