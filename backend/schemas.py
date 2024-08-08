from pydantic import BaseModel, PositiveFloat, EmailStr
from enum import Enum
from datetime import datetime
from typing import Optional

class AvaliacaoBase(BaseModel):
    name: str
    wheight: PositiveFloat
    height: PositiveFloat
    imc: Optional[PositiveFloat]
    result: Optional[str]
    client_email: EmailStr

# Select
class AvaliacaoResponse(AvaliacaoBase): 
    id: int
    refdate: datetime

    class Config: 
        from_attributes = True

# Insert 
class AvaliacaoCreate(AvaliacaoBase): 
    pass

# Update 
class AvalicaoUpdate(BaseModel): 
    name: Optional[str] = None
    wheight: Optional[PositiveFloat] = None
    height: Optional[PositiveFloat] = None
    imc: Optional[PositiveFloat] = None
    result: Optional[str] = None
    client_email: Optional[EmailStr] = None