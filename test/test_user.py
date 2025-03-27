from database import get_db
from main import app
from routers.auth import get_current_user
from fastapi import status
from test.utils import *


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user_authenticated(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "badestcodertest"
    assert response.json()["email"] == "badestcodertest@gmail.com"
    assert response.json()["first_name"] == "Badest"
    assert response.json()["last_name"] == "CoderTest"

def test_change_password_success(test_user):
    response = client.put("/user/password", json={"password":"testpassword", "new_password":"newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_error(test_user):
    response = client.put("/user/password", json={"password":"wrongpassword", "new_password":"newpassword"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail" : 'Error on password chamge'}
    