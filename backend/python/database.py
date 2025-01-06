from dotenv import load_dotenv
import os

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
import bcrypt

from python.models import Base, User, Document_type, Document

load_dotenv()
db_url = os.getenv("DATABASE_URL") 
#env = os.getenv("ENVIRONMENT")

# Připojení k databázi (SQlite pro dev, PGSQL pro prod)
#engine = create_engine(db_url, echo=True)
engine = create_engine(db_url)

# Funkce pro vytvoření všech tabulek
def createTables():
    Base.metadata.create_all(engine)

#naplní všechny číselníky výchozími hodnotami
def fill_catalogs():    
    add_document_types() # číselník typů dokumentů

# přidání číselníku typu dokumentů
def add_document_types ():
    session = Session(engine)
    document_types = ["Občanský průkaz", "Řidičský průkaz", "Zbrojní průkaz", "Odborná způsobilost", "Zdravotní způsobilost", "STK", "Dálniční známka", "Ostatní"]
    
    for document_type in document_types:
        stmt = select(Document_type).where(Document_type.name == document_type).order_by(Document_type.id)
        existing_document_type = session.execute(stmt).scalars().first()

        if not existing_document_type:
            new_document_type = Document_type(
                name = document_type
            )
            session.add(new_document_type)
            session.commit()

    session.close()

def get_document_types():
    session = Session(engine)
    document_types = []

    stmt = select(Document_type).order_by(Document_type.id)
    existing_document_type = session.execute(stmt).scalars().all()

    for d in existing_document_type:
        type = {}
        type["id"] = d.id
        type["name"] = d.name
        document_types.append(type)
        
    session.close() 
    return document_types

def add_document(name, document_type_id, user_id, date_expiration, notify):
    session = Session(engine)

    new_document = Document(
        name = name,
        document_type_id = document_type_id,
        user_id = user_id,
        date_expiration = date_expiration,
        notify = notify
    )

    try:
        session.add(new_document)
        session.commit() 
        session.close()
        return {"success": True, "message":f'Document {name} byl úspěšně vytvořen.'}
    except Exception as e:
        # print(f"Error while committing: {e}")
        session.rollback()
    return True   

def get_documents_for_id(user_id):
    session = Session(engine)

    #takto vypisuje vsechny sloupce, vcetne hesla...
    #stmt = select(User).order_by(User.lastName)
    #users = session.execute(stmt).scalars().all()
    # stmt = (
    #     select(Document.name, Document.document_type_id, Document.date_expiration, Document.notify)
    #         .join(Document_type.name)
    #         .where(Document_type.id == Document.document_type_id)
    #         .where(Document.user_id == user_id)
    #         .order_by(Document.id)
    # )
    stmt = (
        select(
            Document.name,
            Document.document_type_id,
            Document_type.name.label("document_type_name"), #vytvori v selectu sloupec s aliasem document_type_name
            Document.date_expiration,
            Document.notify,
            #User.email.label("user_email")  # informace o uživateli
        )
        .join(Document_type, Document.document_type_id == Document_type.id)  # Join na ciselnik c_document_type
        #.join(User, Document.user_id == User.id)  # Join na tabulku ssers
        .where(Document.user_id == user_id)
        .order_by(Document.id)
    )
    result = session.execute(stmt).all()
    
    if not result:
        return None
    
    documents = []
    for row in result:
        name, document_type_id, document_type, date_expiration, notify = row
        document = {"name":name, "document_type_id": document_type_id, "document_type": document_type, "date_expiration":date_expiration, "notify":notify}
        documents.append(document)
    
    session.close()
    return documents        

def addUser(email, password, firstName, lastName, disabled):
    if getUser (email):
        print (f"AddUser: Uživatel {email} již existuje.")
        return {"success": False, "message":f'AddUser: Uživatel {email} již existuje.'}

    session = Session(engine)

    new_user = User(
        email = email,
        password = password,
        firstName = firstName,
        lastName = lastName,
        disabled = disabled
    )

    try:
        session.add(new_user)
        session.commit()  # Uložení změn do databáze
        #print(f"AddUser: Uživatel {email} byl úspěšně přidán.")
        session.close()
        return {"success": True, "message":f'Uživatel {email} byl úspěšně vytvořen.'}
    except Exception as e:
        # print(f"Error while committing: {e}")
        session.rollback()
    return True


def getUsers ():
    session = Session(engine)

    #takto vypisuje vsechny sloupce, vcetne hesla...
    #stmt = select(User).order_by(User.lastName)
    #users = session.execute(stmt).scalars().all()
    stmt = select(User.email, User.firstName, User.lastName, User.disabled).order_by(User.lastName)
    result = session.execute(stmt).all()
    
    if not result:
        return None
    
    users = []

    for row in result:
        email, firstName, lastName, disabled = row
        user = {"email":email, "firstName": firstName, "lastName":lastName, "disabled":disabled}
        users.append(user)
    
    session.close()
    return users    

def getUser (email):
    session = Session(engine)

    stmt = select(User).where(User.email == email)
    user = session.execute(stmt).scalars().first()

    if not user:
        return None

    session.close()
    return user

def verifyPassword (plainPassword, hashedPassword):
    passwordBytes = plainPassword.encode('utf-8') # converting password to array of bytes (to same jako b'asd' ) 
    return bcrypt.checkpw(passwordBytes, hashedPassword)     

def getPasswordHash(password):
    passwordBytes = password.encode('utf-8') 

    salt = bcrypt.gensalt() 
    return bcrypt.hashpw(passwordBytes, salt) 

def authenticatedUser (email, password):
    session = Session(engine)
    
    user = getUser (email)
    session.close()
    
    if not user:
        print(f"Uživatel {email} neexistuje.")
        return None
    
    if user.disabled:
        print(f"Uživatel {email} je zablokován.")
        return 403

    if verifyPassword(password, user.password):
        print(f"Uživatel {email} je ověřen.")
        return user
    else:
        print(f"Neplatné přihlašovací údaje pro {email}.")
        return None

