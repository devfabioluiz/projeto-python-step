import bcrypt
import jwt
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Usuario
from api.schemas import UsuarioRegistrar, UsuarioLogin
from api.middlewares import JWT_SECRET, autenticar, admin, limiter

router = APIRouter()


@router.get("/")
@router.get("/api")
@limiter.limit("100/minute")
async def root(request: Request):
    return {
        "mensagem": "API do Projeto Final Python funcionando!",
        "versao": "1.0.0",
    }


@router.get("/favicon.ico")
async def favicon():
    return JSONResponse(status_code=204)


@router.post("/api/registrar")
@limiter.limit("10/minute")
async def registrar(
    dados: UsuarioRegistrar,
    request: Request,
    db: Session = Depends(get_db),
):
    existe = db.query(Usuario).filter(Usuario.email == dados.email).first()

    if existe:
        return JSONResponse(status_code=400, content={"erro": "Email já cadastrado"})

    senha_hash = bcrypt.hashpw(
        dados.senha.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha=senha_hash,
        role=dados.role,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    token = jwt.encode(
        {
            "id": usuario.id,
            "email": usuario.email,
            "role": usuario.role,
        },
        JWT_SECRET,
        algorithm="HS256",
    )

    return JSONResponse(status_code=201, content={
        "mensagem": "Usuário registrado com sucesso",
        "token": token,
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "role": usuario.role,
        },
    })


@router.post("/api/login")
@limiter.limit("10/minute")
async def login(
    dados: UsuarioLogin,
    request: Request,
    db: Session = Depends(get_db),
):
    usuario = db.query(Usuario).filter(Usuario.email == dados.email).first()

    if not usuario:
        return JSONResponse(status_code=401, content={"erro": "Email ou senha inválidos"})

    senha_valida = bcrypt.checkpw(
        dados.senha.encode("utf-8"), usuario.senha.encode("utf-8")
    )

    if not senha_valida:
        return JSONResponse(status_code=401, content={"erro": "Email ou senha inválidos"})

    token = jwt.encode(
        {
            "id": usuario.id,
            "email": usuario.email,
            "role": usuario.role,
        },
        JWT_SECRET,
        algorithm="HS256",
    )

    return {
        "mensagem": "Login realizado com sucesso",
        "token": token,
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "role": usuario.role,
        },
    }


@router.get("/api/me")
async def perfil(
    request: Request,
    db: Session = Depends(get_db),
    _=Depends(autenticar),
):
    usuario = db.query(Usuario).filter(
        Usuario.id == request.state.usuario_id
    ).first()

    if not usuario:
        return JSONResponse(status_code=404, content={"erro": "Usuário não encontrado"})

    return {
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "role": usuario.role,
        },
    }
