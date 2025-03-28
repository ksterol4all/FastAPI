import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()
""" 
#SQLite database connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}) 
"""

""" 
#MySQL database connection
password = quote_plus("")
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:{password}@127.0.0.1:3306/TodoApplicationDatabase"
engine = create_engine(SQLALCHEMY_DATABASE_URL) 
"""

#Postgresql database connection
SQLALCHEMY_DATABASE_URL = os.getenv("POSTGRESQL_DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("No POSTGRESQL_DATABASE_URL found in environment variables. Please add it to your .env file.")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
#Postgresql database connection

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
