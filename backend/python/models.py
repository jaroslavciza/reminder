# from sqlalchemy import Column, String, LargeBinary, Boolean, ForeignKey

import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# from sqlalchemy.ext.declarative import declarative_base

from pydantic import BaseModel, EmailStr

# DB modely
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    def __str__(self): #print as
        return f"User: {self.email}"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] #pokud neposilam zadne parametry, nemusim pouzivat mapped_column() vubec
    password: Mapped[bytes] 
    firstName: Mapped[str] = mapped_column(nullable=True)
    lastName: Mapped[str] = mapped_column(nullable=True)
    disabled: Mapped[bool] = mapped_column(default=False)
    documents: Mapped [list["Document"]] = relationship()

class Document (Base):
    __tablename__ = "documents"

    def __str__(self): #print as
        return f"Document: {self.owner} - {self.name}"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True) 
    name: Mapped[str] = mapped_column(nullable=True)
    document_type_id: Mapped[int] = mapped_column(ForeignKey("c_document_type.id"))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    date_expiration: Mapped[datetime.date]
    notify: Mapped[bool] = mapped_column(default=False) 

class Document_type (Base):
    __tablename__ = "c_document_type"

    def __str__(self):
        return f"Document_type: {self.name}"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True) 
    name: Mapped[str]


# modely pro JWT token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None



# modely Form pro posilani z frontendu
class FormRegisterUser (BaseModel):
    email: EmailStr
    password: str
    firstName: str
    lastName: str

class FormAddDocument (BaseModel):
    document_type: int
    document_name: str
    document_date_expiration: datetime.date
    document_notify: bool