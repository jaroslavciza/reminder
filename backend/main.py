import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# passlib neni updateovani a s novou verzi bcrypt hazi chyby, predelal jsem to na pure bcrypt
# from passlib.context import CryptContext
import bcrypt #zasifrovani hesel
import jwt
from jwt.exceptions import InvalidTokenError

# from typing import Dict, Annotated

#from python.database import createTables, addUser, getUser, isUserAthenticated
import python.database as db
from python.models import User, Token, TokenData, FormRegisterUser, FormAddDocument

# import logging

# log = logging.getLogger(__name__)
# logging.basicConfig(
#     #filename='backend.log',
#     level=logging.INFO, #od jake urovne zprav se budou zachytavat log informace
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S")

# log.info('App Started')

# log.DEBUG
# log.INFO
# log.WARNING
# log.ERROR
# log.CRITICAL

load_dotenv()

app = FastAPI() # je postavený na async def takže už asyncio nemusím na async volání používat zvlášť

# Vytvoření tabulek
db.createTables()
db.fill_catalogs() #naplnění číselníků

# kvuli CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",  # Vue.js Dev server
    "https://reminder.ciza.eu",   # production URL
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# run: openssl rand -hex 32
# pouzije se k podepsani JWT tokenu - pozdeji predelat do SECRETS!!!
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
async def root():
    return "API loaded"

# @app.get("/users/{userId}/")
# async def get_user_by_id(userId: str): #název funkce pokud je s _ zobrazi ve swaggeru jako Get User By Id
#     # user = next((user for user in users if user.get("id") == int(userId)), None)
#     # if user:
#     #     return user
#     return {}

def createAccessToken(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def getCurrentUser(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        #JWT je signed! tzn muzeme overit, ze jsme ho vytvorili my pomoci SECRET_KEY
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        # print ("JWT username:", email)
        if email is None:
            raise credentials_exception
        tokenData = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception

    user = db.getUser(email=tokenData.email)

    if user is None:
        raise credentials_exception

    return user

async def getCurrentActiveUser(currentUser: User = Depends(getCurrentUser)):
    if currentUser.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return currentUser

@app.post("/token")
async def login_for_access_token(formData: OAuth2PasswordRequestForm = Depends()):
    user = db.authenticatedUser(formData.username, formData.password)

    if user == 403:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is disabled",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = createAccessToken(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

#pro endpoint /login - vypada to lepe z frontendu nez /token
@app.post("/login")
async def login_via_frontend (formData: OAuth2PasswordRequestForm = Depends()):
    return await login_for_access_token(formData)

@app.post("/register")
async def register_new_account (formData: FormRegisterUser):
    hasshedPassword = db.getPasswordHash(formData.password)
    user = db.addUser(formData.email, hasshedPassword, formData.firstName, formData.lastName, False)

    if not user:
        return {"success": False, "message": "Neznámá chyba při registraci."}   

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = createAccessToken(
        data={"sub": formData.email}, expires_delta=access_token_expires
    )
    
    return {"success": True, "message": user["message"], "access_token": access_token}

@app.get("/users")
async def get_users(currentUser: User = Depends(getCurrentActiveUser)):
    if not currentUser:
        raise HTTPException(status_code=401, detail="Unauthorized")

    users = db.getUsers()

    if not users:
        return None

    return users

@app.get("/document_types")
async def get_document_types():
    document_types = db.get_document_types()

    if not document_types:
        return None

    return document_types

@app.get("/get_documents")
async def get_my_documents(current_user: User = Depends(getCurrentActiveUser)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    documents = db.get_documents_for_id(current_user.id)

    if not documents:
        return None
    
    return documents

@app.post("/add_document")
async def add_document(formData: FormAddDocument, current_user: User = Depends(getCurrentActiveUser)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    document = db.add_document(formData.document_name, formData.document_type, current_user.id, formData.document_date_expiration, formData.document_notify)

    if document:
        return {"success": True, "message": f"Dokument {formData.document_name} uložen."}
    return {"success": False, "message": f"Dokument {formData.document_name} se nepodařilo uložit."}

