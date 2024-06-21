from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
import secrets
from sqlalchemy import Column, String, Boolean, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# SQLite database URL
DATABASE_URL = "sqlite:///./etechnosoft.db"

# Database setup
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Utility functions
def generate_random_hex(bytes_length=32):
    """
    Generate a random hexadecimal string.

    Args:
        
        bytes_length (int): The length of the string in bytes.

    Returns:
        
        str: A random hexadecimal string.
    """
    return secrets.token_hex(bytes_length)

def generate_client_id():
    """
    Generate a random client ID.

    Returns:
        
        str: A random client ID in uppercase.
    """
    return secrets.token_hex(7).upper()

# User model
class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    activated = Column(Boolean, default=False)
    secret_key = Column(String, unique=True, index=True)
    client_id = Column(String, unique=True, index=True)

Base.metadata.create_all(bind=engine)

# Pydantic models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    activated: bool | None = None

class UserInDB(User):
    hashed_password: str

class RegisterUserRequest(BaseModel):
    username: str
    email: str
    password: str

class RegistrationResponseModel(BaseModel):
    username: str
    email: str
    secret_key: str
    client_id: str

class GeneralResponseModel(BaseModel):
    isSuccessful: bool
    message: str
    data: list = []

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Dependency
def get_db():
    """
    Get a new database session.

    Yields:
        
        Session: A new database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utility functions
def verify_password(plain_password, hashed_password):
    """
    Verify a password against a hashed password.

    Args:
        
        plain_password (str): The plain password.
        
        hashed_password (str): The hashed password.

    Returns:
        
        bool: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Hash a password.

    Args:
        
        password (str): The password to hash.

    Returns:
        
        str: The hashed password.
    """
    return pwd_context.hash(password)

def get_user(db: Session, username: str):
    """
    Get a user by username.

    Args:
        
        db (Session): The database session.
        
        username (str): The username.

    Returns:
        
        UserModel | None: The user if found, None otherwise.
    """
    return db.query(UserModel).filter(UserModel.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    """
    Authenticate a user.

    Args:
        
        db (Session): The database session.
        
        username (str): The username.
        
        password (str): The password.

    Returns:
        
        UserModel | bool: The user if authentication is successful, False otherwise.
    """
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, secret_key: str, expires_delta: timedelta | None = None):
    """
    Create a new access token.

    Args:
        
        data (dict): The data to encode in the token.
        
        secret_key (str): The secret key to sign the token.
        
        expires_delta (timedelta, optional): The token's expiry time. Defaults to 15 minutes.

    Returns:
        
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt

# Helper function to get the current user
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    """
    Get the current user from the token.

    Args:
        
        token (str): The JWT token.
        
        db (Session): The database session.

    Returns:
        
        UserModel: The current user.

    Raises:
        
        HTTPException: If the credentials are invalid.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        unverified_payload = jwt.decode(token, options={"verify_signature": False})
        username: str = unverified_payload.get("sub")
        if username is None:
            raise credentials_exception
        user = get_user(db, username=username)
        if user is None:
            raise credentials_exception
        payload = jwt.decode(token, user.secret_key, algorithms=[ALGORITHM])
    except InvalidTokenError:
        raise credentials_exception
    return user

# Helper function to get the current active user
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Get the current active user.

    Args:
    
        current_user (User): The current user.

    Returns:
        
        User: The current active user.

    Raises:
    
        HTTPException: If the user is inactive.
    """
    if not current_user.activated:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Endpoints
@app.post("/register", response_model=RegistrationResponseModel, tags=['Authentication'])
def register_user(request: RegisterUserRequest, db: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
        request (RegisterUserRequest): The registration request.
        
        db (Session): The database session.

    Returns:
    
        RegistrationResponseModel: The registration response.
    """
    hashed_password = get_password_hash(request.password)
    secret_key = generate_random_hex()
    client_id = generate_client_id()
    user = UserModel(
        username=request.username,
        email=request.email,
        hashed_password=hashed_password,
        secret_key=secret_key,
        client_id=client_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return RegistrationResponseModel(username=user.username, 
                                     email=user.email, 
                                     secret_key=user.secret_key, 
                                     client_id=user.client_id)

@app.post("/token", response_model=Token, tags=['Authentication'])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> Token:
    """
    Login for access token.

    Args:
        
        form_data (OAuth2PasswordRequestForm): The login form data.
        
        db (Session): The database session.

    Returns:
        
        Token: The access token.

    Raises:
        
        HTTPException: If the username or password is incorrect.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, secret_key=user.secret_key, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/retrieve-access-token", response_model=GeneralResponseModel, tags=['Authentication'])
async def retrieve_access_token(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    Retrieve a new access token.

    Args:
        
        current_user (User): The current active user.
        
        db (Session): The database session.

    Returns:
        
        GeneralResponseModel: The response with the new token.
    """
    user = get_user(db, current_user.username)
    token = create_access_token(data={"sub": current_user.username}, secret_key=user.secret_key)
    return GeneralResponseModel(isSuccessful=True, message="Token retrieved successfully", data=[token])


@app.post("/account-activation", response_model=GeneralResponseModel, tags=['Authentication'])
async def account_activation(
    token: str,
    db: Session = Depends(get_db)
):
    """
    Activate a user account.

    Args:
        
        token (str) : The activation token.
        
        db (Session) : The database session.

    Returns:
        
        GeneralResponseModel: The response indicating the account activation status.

    Raises:
        
        HTTPException : If the credentials are invalid.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        unverified_payload = jwt.decode(token, options={"verify_signature": False})
        username: str = unverified_payload.get("sub")
        if username is None:
            raise credentials_exception
        user = get_user(db, username=username)
        if user is None:
            raise credentials_exception
        payload = jwt.decode(token, user.secret_key, algorithms=[ALGORITHM])
    except InvalidTokenError:
        raise credentials_exception

    user.activated = True
    db.commit()
    db.refresh(user)
    return GeneralResponseModel(isSuccessful=True, message="Account activated successfully")

@app.get("/users/me/", response_model=User, tags=['Authentication'])
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Get the current user's details.

    Args:
        
        current_user (User): The current active user.

    Returns:
        
        User: The current user's details.
    """
    return current_user


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
