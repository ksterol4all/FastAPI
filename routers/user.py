from typing import Optional, Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Path, Query, HTTPException, Depends
from pydantic import BaseModel, Field
from starlette import status
from models import Users
from database import get_db
from .auth import get_current_user
from passlib.context import CryptContext


router = APIRouter(
    prefix='/user',
    tags=['User Management']
)


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserVerificationRequest(BaseModel):
    password: str = Field(..., min_length=8, max_length=255, title="Password")
    new_password: str = Field(..., min_length=8, max_length=255, title="New Password")


def unauthorized_exception(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication fail')
    


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    unauthorized_exception(user)

    user = db.query(Users).filter(Users.id == user.get('id')).first()
    
    if user is not None:
        return user
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerificationRequest):
    unauthorized_exception(user)
    
    user = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error on password chamge")
    
    user.hashed_password = bcrypt_context.hash(user_verification.new_password)

    db.add(user)
    db.commit()
    return {"message": "User updated successfully"} 

@router.put("/phone_number/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(user: user_dependency, db: db_dependency, phone_number: str):
    unauthorized_exception(user)
    
    user = db.query(Users).filter(Users.id == user.get('id')).first()
    
    user.phone_number = phone_number

    db.add(user)
    db.commit()
    return {"message": "User updated successfully"} 

