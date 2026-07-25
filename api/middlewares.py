import jwt
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from dotenv import load_dotenv
import os

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "minha-chave-secreta-super-segura")

limiter = Limiter(key_func=get_remote_address)


def autenticar(request: Request):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(status_code=401, detail="Token não informado")

    try:
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        request.state.usuario_id = payload["id"]
        request.state.usuario_email = payload["email"]
        request.state.usuario_role = payload.get("role", "user")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


def admin(request: Request):
    if request.state.usuario_role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Acesso restrito a administradores",
        )


def registrar_exception_handlers(app):
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"erro": "Erro interno do servidor"},
        )

    app.add_exception_handler(429, _rate_limit_exceeded_handler)


def configurar_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
