from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base

class AvaliacaoModel(Base):
    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    wheight = Column(Float)
    height = Column(Float)
    imc = Column(Float)
    result = Column(String)
    client_email = Column(String)
    refdate = Column(DateTime(timezone=True), default=func.now())