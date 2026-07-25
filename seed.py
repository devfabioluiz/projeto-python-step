from dotenv import load_dotenv
from api.database import Base, get_engine
from api.models import Usuario
from sqlalchemy.orm import sessionmaker
import bcrypt

load_dotenv()


def seed():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    if db.query(Usuario).count() > 0:
        print("Banco já populado. Pulando seed.")
        db.close()
        return

    senha_hash = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode("utf-8")

    db.add_all([
        Usuario(nome="Admin", email="admin@email.com", senha=senha_hash, role="admin"),
        Usuario(nome="Usuário Teste", email="user@email.com", senha=senha_hash, role="user"),
    ])

    db.commit()
    db.close()

    print("Seed concluído!")
    print("Admin: admin@email.com / senha: admin123")
    print("User:  user@email.com / senha: admin123")


if __name__ == "__main__":
    seed()
