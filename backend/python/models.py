from sqlalchemy import Column, String, LargeBinary, Boolean
from sqlalchemy.ext.declarative import declarative_base

from pydantic import BaseModel, EmailStr

#DB model
Base = declarative_base()
class User(Base):
    __tablename__ = "users"

    def __str__(self): #print as
        return f"User: {self.email}"
    
    email = Column(String(255), primary_key=True)
    password = Column(LargeBinary, nullable=False)
    firstName = Column(String(255), nullable=True)
    lastName = Column(String(255), nullable=True)
    disabled = Column(Boolean, default=False, nullable=False)

# modely pro JWT token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

# modely Form z frontendu pro registraci uzivatele
class RegisterUser (BaseModel):
    email: EmailStr
    password: str
    firstName: str
    lastName: str