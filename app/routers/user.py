from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends, APIRouter, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, select
from app.database import get_db
from app.models.user import User
from app.models.dataset import Dataset, DatasetRows
from app.schemas.user import UserCreate, UserResponse
from app.schemas.dataset import DatasetStatusResponse, DatasetRowResponse
from app.services.user_service import *
from app.schemas.user import *


router = APIRouter(prefix="/user", tags=["User"])

@router.post("/register") 
async def register(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db=db)

    
@router.post("/login")
async def login(formdata: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # existing_user = db.execute(select(User).where(User.email == user.email)).scalar_one_or_none()
    user = get_user_by_email(formdata.username, db)
    if user and verify_password(formdata.password, user.hashed_password):
        token = create_token({"sub": str(user.username)})
        return {"access_token": token, "token_type": "Bearer"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")
    