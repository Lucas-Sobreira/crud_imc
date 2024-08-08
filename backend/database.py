from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

POSTGRES_DATABASE_URL = "postgresql://user:password@postgres/mydatabase"
engine = create_engine(POSTGRES_DATABASE_URL)

# SQLALCHEMY_DATABASE_UTL = "sqlite:///./imc_avaliacoes.db"
# engine = create_engine(SQLALCHEMY_DATABASE_UTL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db # retorna a Sessão Instanciada
    finally:
        db.close()