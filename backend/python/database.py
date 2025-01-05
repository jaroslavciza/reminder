from dotenv import load_dotenv
import os

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
import bcrypt

from python.models import Base, User

load_dotenv(verbose=True)
db_url = os.getenv("DATABASE_URL") 
#env = os.getenv("ENVIRONMENT")

# Připojení k SQLite databázi
engine = create_engine(db_url)

# Funkce pro vytvoření všech tabulek
def createTables():

    Base.metadata.create_all(engine)

# Funkce pro získání session
def getSession():
    # Inicializace sessionmakeru
    Session = sessionmaker(bind=engine)    
    return Session()


def addUser(email, password, firstName, lastName, disabled):
    session = getSession()  # Získání nové session

    new_user = User(
        email = email,
        password = password,
        firstName = firstName,
        lastName = lastName,
        disabled = disabled
    )

    if getUser (email):
        print (f"AddUser: Uživatel {email} již existuje.")
        return {"success": False, "message":f'AddUser: Uživatel {email} již existuje.'}

    try:
        session.add(new_user)
        session.commit()  # Uložení změn do databáze
        #print(f"AddUser: Uživatel {email} byl úspěšně přidán.")
        session.close()
        return {"success": True, "message":f'Uživatel {email} byl úspěšně vytvořen.'}
    except Exception as e:
        # print(f"Error while committing: {e}")
        session.rollback()

    return


def getUsers ():
    session = getSession()
    
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
    session = getSession()
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
    session = getSession()
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

