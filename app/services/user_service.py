from passlib.context import CryptContext
import os
from dotenv import load_dotenv
load_dotenv()
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, select
from app.database import get_db
from app.models.user import User
from app.models.dataset import Dataset, DatasetRows
from app.schemas.user import UserCreate, UserResponse
from app.schemas.dataset import DatasetStatusResponse, DatasetRowResponse
from datetime import datetime, timedelta, timezone

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login") #?Login Endpoint
pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password: str):
    return pwd_context.hash(password[:72])

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password[:72], hashed_password)

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

async def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):

    payload = verify_token(token)
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    # user = db.query(User).filter(User.username == username).first()
    user = db.execute(select(User).where(User.username == username)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

        

def create_user(user: UserCreate, db: Session):
    # existing_user = db.query(User).filter(or_(User.email == user.email, User.username == user.username)).first()
    existing_user = db.execute(select(User).where(or_(User.email == user.email, User.username == user.username))).scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    # new_user = User(username=user.username, hashed_password=hash_password(user.password), email=user.email)
    new_user = User(username=user.username, hashed_password=hash_password(user.password), email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserResponse.model_validate(new_user)

def get_user_by_email(email: str, db: Session):
    # return db.query(User).filter(User.email == email).first()
    return db.execute(select(User).where(User.email == email)).scalar_one_or_none()

def get_user_by_username(username: str, db: Session):
    # return db.query(User).filter(User.username == username).first()
    return db.execute(select(User).where(User.username == username)).scalar_one_or_none()

def get_user_by_id(user_id: str, db: Session):
    # return db.query(User).filter(User.id == user_id).first()
    return db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()