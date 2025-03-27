from urllib.parse import quote_plus
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine, text
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app
import pytest
from models import Todos, Users
from routers.auth import bcrypt_context


SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}, poolclass=StaticPool) 

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {"username": "badestcoder@gmail.com", "id": 1, "user_role": "Admin"}


client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todos(
        title="learn to code",
        description="need to learn to code everyday to become better",
        priority=5,
        complete=False,
        user_id=1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM todos;"))
        conn.commit()

@pytest.fixture
def test_user():
    user = Users(
        email = "badestcodertest@gmail.com",
        username = "badestcodertest",
        first_name = "Badest",
        last_name = "CoderTest",
        hashed_password = bcrypt_context.hash("testpassword"),
        is_active = True,
        role = "Admin",
        phone_number = "7645453548"
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM users;"))
        conn.commit()