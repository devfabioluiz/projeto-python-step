from pydantic import BaseModel


class UsuarioRegistrar(BaseModel):
    nome: str
    email: str
    senha: str
    role: str = "user"


class UsuarioLogin(BaseModel):
    email: str
    senha: str
