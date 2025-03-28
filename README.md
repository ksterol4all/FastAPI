# FastAPI Todo App

This is a simple Todo application built using FastAPI, SQLAlchemy, Jinja2 templates, and PostgreSQL. The application supports user authentication, CRUD operations on todos, and integration with Render.com as a PostgreSQL database host.


## Features
- User Registration and Login (JWT Authentication)
- Create, Read, Update, Delete (CRUD) operations for Todos
- Integration with PostgreSQL (Hosted on Render.com)
- FastAPI Dependency Injection
- Jinja2 Template Rendering
- Logging for tracking API requests and handling errors
- Use of FastAPI Routers for better code organization
- Custom `.gitignore` file to avoid sensitive files being pushed

---

## Project Structure
```
/ToDoApp
|-- /routers
|   |-- auth.py       (Handles Authentication and User Management)
|   |-- todos.py      (CRUD operations for Todos)
|   |-- admin.py      (Admin functionalities)
|   |-- user.py       (User management functionalities)
|-- /static           (Static files like CSS, JS)
|-- /templates        (HTML templates)
|-- logging_config.py (Configuration for logging)
|-- main.py           (Main application entry point)
|-- models.py         (Database models using SQLAlchemy)
|-- database.py       (Database configuration and connection)
|-- .gitignore        (List of files and folders to be ignored)
```

---

## Requirements
- Python 3.12+
- FastAPI
- SQLAlchemy
- Jinja2
- psycopg2
- passlib (for password hashing)
- PyJWT (for JWT Authentication)
- Uvicorn (for running the FastAPI server)
- pgAdmin (for managing PostgreSQL databases)

---

## Installation
1. **Clone the repository**
```bash
git clone <your-repo-url>
cd ToDoApp
```

2. **Create a virtual environment and activate it**
```bash
python -m venv fastapienv
fastapienv\Scripts\activate   # On Windows
source fastapienv/bin/activate  # On Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

---

## Configuration
Create a `.env` file to store your PostgreSQL credentials:
```
POSTGRESQL_DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database_name>
SECRET_KEY=your_secret_key
ALGORITHM=HS256
```

Update your `database.py` file to read from this `.env` file.

---

## Database Migration
You can use the sqlite by uncomment the connection and commenting the postgres but if you are using a PostgreSQL database, then pass in your credentials or you can use PostgreSQL database hosted on Render.com, ensure your connection URL is correctly set in your `.env` file. You can test your connection using `pgAdmin` as explained above.

---

## Running the Application
To start the FastAPI application:
```bash
uvicorn main:app --reload
```
Visit `http://127.0.0.1:8000` to access the application.

---

## Endpoints
### Authentication
- `POST /auth/` - Register a new user
- `POST /auth/token` - Authenticate and obtain JWT token
- `GET /auth/login-page` - Render login page
- `GET /auth/register-page` - Render registration page

### Todos
- `POST /todos/todo/` - Create a new todo
- `GET /todos/` - Retrieve all todos
- `GET /todos/todo/{id}` - Retrieve a specific todo by ID
- `PUT /todos/todo/{id}` - Update a todo
- `DELETE /todos/todo/{id}` - Delete a todo

---

## Deployment
To deploy your application, you can use Render.com, Docker, or any cloud service that supports FastAPI.

### Render.com Deployment (Optional)
1. Push your code to GitHub.
2. Create a new **Web Service** on Render.com and connect your GitHub repo.
3. Set your environment variables (from `.env`) in the Render.com dashboard.
4. Deploy and monitor logs.

---

## Contributing
Feel free to open issues or submit pull requests if you would like to contribute.

---

## Live Deployment for testing
https://todo-deployment-n7fr.onrender.com/


