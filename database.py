from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


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
SQLALCHEMY_DATABASE_URL = "postgresql://admin:Nq6TkK5G052I5LWtKxTbFqlEdGlxbpP6@dpg-cviukjjuibrs738um6a0-a.ohio-postgres.render.com/todo_db_743k"
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
