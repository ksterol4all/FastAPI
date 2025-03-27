from typing import Optional, Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Path, Query, HTTPException, Depends
from pydantic import BaseModel, Field
from starlette import status
from models import Todos
from database import get_db
from .auth import get_current_user


router = APIRouter(
    prefix='/admin',
    tags=['Admin Management']
)



db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


def unauthorized_exception(user: user_dependency):
    if user is None or user.get('user_role').casefold() != 'admin'.casefold():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication fail')
    


@router.get("/todo", status_code=status.HTTP_200_OK)
async def get_all(user: user_dependency, db: db_dependency):
    unauthorized_exception(user)
    
    return db.query(Todos).all()

@router.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(user: user_dependency, db: db_dependency, id: int = Path(gt=0)):
    unauthorized_exception(user)

    todo = db.query(Todos).filter(Todos.id == id).first()
    
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}

