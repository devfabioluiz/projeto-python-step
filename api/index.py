from fastapi import FastAPI
from api.database import Base, engine
from api.routes import router
from api.middlewares import (
    configurar_cors,
    registrar_exception_handlers,
    limiter,
)
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="API Python - Projeto Final", version="1.0.0")

configurar_cors(app)
registrar_exception_handlers(app)

app.state.limiter = limiter

app.include_router(router)


@app.on_event("startup")
def criar_tabelas():
    Base.metadata.create_all(bind=engine)
