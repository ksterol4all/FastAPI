from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models import Users
from passlib.context import CryptContext
from database import get_db
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)


SECRET_KEY = '625558a744477869857bc3c0d2e637bf5fb4766250bb9d27b645877815322c30'
ALGORITHM = 'HS256'


db_dependency = Annotated[Session, Depends(get_db)]
form_data = Annotated[OAuth2PasswordRequestForm, Depends()]

templates = Jinja2Templates(directory="templates")

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto') #used for hashing password
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
token_bearer = Annotated[str, Depends(oauth2_bearer)]




### Pages ###
@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})



### Endpoints ###
def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return False
    
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    
    return user

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {
        'sub' : username,
        'id': user_id,
        'role': role
    }

    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: token_bearer):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate user")
        
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate user")


class UserRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=255, title="Username")
    email: str = Field(..., min_length=10, max_length=255, title="Description")
    first_name: str = Field(..., min_length=3, max_length=255, title="Description")
    last_name: str = Field(..., min_length=3, max_length=255, title="Description")
    password: str = Field(..., min_length=7, max_length=255, title="Description")
    role: str = Field(..., min_length=3, max_length=255, title="Description")
    phone_number: str = Field(..., min_length=9, max_length=20, title="Description")

class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/",  status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency, userRequest: UserRequest):
    user = Users(
        email = userRequest.email,
        username = userRequest.username,
        first_name = userRequest.first_name,
        last_name = userRequest.last_name,
        hashed_password = bcrypt_context.hash(userRequest.password),
        role = userRequest.role,
        is_active = True,
        phone_number = userRequest.phone_number
    )

    db.add(user)
    db.commit()
    return {"message": "User created successfully"}

@router.post("/token", response_model=Token, status_code=status.HTTP_201_CREATED)
async def login_for_acces_token(db:db_dependency, fd: form_data):
    user = authenticate_user(fd.username, fd.password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate user")
    
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}