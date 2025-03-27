from typing import Optional, Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Path, Query, HTTPException, Depends, Request
from pydantic import BaseModel, Field
from starlette import status
from starlette.responses import RedirectResponse
from models import Todos
from database import get_db
from .auth import get_current_user
from fastapi.templating import Jinja2Templates
from logging_config import logger


router = APIRouter(
    prefix='/todos',
    tags=['Todo Management']
)


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

templates = Jinja2Templates(directory="templates")


class TodoRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=255, title="Todo Title", description="The title of the Todo")
    description: str = Field(..., min_length=10, max_length=1000, title="Description", description="A short description of the Todo")
    priority: int = Field(..., ge=0, le=5, title="Priority", description="priority of the Todo, from 0 to 5")
    complete: bool = Field(..., title="Complete", description="Is the Todo completed")


    model_config = {
        "json_schema_extra": {
            "example" :{
                "title" : "Todo Title",
                "description" : "A short description of the todo",
                "priority" : 3,
                "complete" : False
            }
        }
    }


def unauthorized_exception(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication fail')


def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page", status_code= status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")

    return redirect_response


### Pages ###
@router.get("/todo-page")
async def render_todo_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()
        
        todos = db.query(Todos).filter(Todos.user_id == user.get("id")).all()

        return templates.TemplateResponse("todo.html", {"request": request, "todos": todos, "user": user})
    except:
        return redirect_to_login()

@router.get("/add-todo-page")
async def render_add_todo_page(request: Request):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()

        return templates.TemplateResponse("add-todo.html", {"request": request, "user": user})
    except:
        return redirect_to_login()

@router.get("/edit-todo-page/{todo_id}")
async def render_edit_todo_page(request: Request, todo_id: int,  db: db_dependency):
    try:
        logger.info(f"Received request to edit todo with ID: {todo_id}")

        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            logger.warning("User authentication failed. Redirecting to login.")
            return redirect_to_login()

        logger.info(f"User authenticated successfully: {user['username']}")
        todo = db.query(Todos).filter(Todos.id == todo_id).first()

        if todo is None:
            logger.error(f"Todo with ID {todo_id} not found in the database.")
            return redirect_to_login()
        
        logger.info(f"Todo with ID {todo_id} found: {todo.title}")

        return templates.TemplateResponse("edit-todo.html", {"request": request, "todo":todo, "user": user})
    except Exception as e:
        logger.exception(f"Exception occurred while rendering edit-todo-page: {str(e)}")
        return redirect_to_login()
    




### Endpoints ###
@router.get("/", status_code=status.HTTP_200_OK)
async def get_all(user: user_dependency, db: db_dependency):
    unauthorized_exception(user)
    
    return db.query(Todos).filter(Todos.user_id == user.get('id')).all()


@router.get("/todo/{id}", status_code=status.HTTP_200_OK)
async def get_todo(user: user_dependency, db: db_dependency, id: int = Path(gt=0)):
    unauthorized_exception(user)
    
    todo = db.query(Todos).filter(Todos.id == id).filter(Todos.user_id == user.get('id')).first()
    
    if todo is not None:
            return todo
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

@router.post("/todo/", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    unauthorized_exception(user)
    
    todo = Todos(**todo_request.model_dump(), user_id = user.get('id'))

    db.add(todo)
    db.commit()
    return {"message": "Todo created successfully"}

@router.put("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest, id: int = Path(gt=0)):
    unauthorized_exception(user)
    
    todo = db.query(Todos).filter(Todos.id == id).filter(Todos.user_id == user.get('id')).first()

    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    todo.title = todo_request.title
    todo.description = todo_request.description
    todo.priority = todo_request.priority
    todo.complete = todo_request.complete

    db.add(todo)
    db.commit()
    return {"message": "Todo updated successfully"}

@router.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(user: user_dependency, db: db_dependency, id: int = Path(gt=0)):
    unauthorized_exception(user)

    todo = db.query(Todos).filter(Todos.id == id).filter(Todos.user_id == user.get('id')).first()
    
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}
