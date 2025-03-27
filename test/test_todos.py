from database import get_db
from main import app
from routers.auth import get_current_user
from fastapi import status
from test.utils import *



app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user



def test_read_all_authenticated(test_todo):
    response = client.get("/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"id":1, "title":"learn to code", "description":"need to learn to code everyday to become better", "priority":5, "complete":False, "user_id":1}]

def test_read_one_authenticated(test_todo):
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id":1, "title":"learn to code", "description":"need to learn to code everyday to become better", "priority":5, "complete":False, "user_id":1}