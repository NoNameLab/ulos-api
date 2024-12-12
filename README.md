# API-ULOS-DB

A FastAPI-based project for managing tasks, users, and execution logs, using Tortoise ORM and PostgreSQL. This API provides CRUD operations, task state management, error logging, and more.

![FastAPI Logo](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png)

---

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Running the Project](#running-the-project)
4. [API Endpoints](#api-endpoints)
5. [Swagger UI](#swagger-ui)
6. [Screenshots](#screenshots)
7. [Database Models](#database-models)
8. [Contributing](#contributing)
9. [License](#license)

---

## Features

- **User, Machines, Files and Metrics Management**: CRUD operations for users and the others.
- **Task Management**: Create, update, delete tasks, and manage their states.
- **State Tracking**: Group and filter tasks by their state.
- **Error Simulation**: Simulate errors and log them with detailed messages.
- **Database Integration**: Uses PostgreSQL with Tortoise ORM.
- **Automatic Documentation**: Swagger UI and ReDoc.

---

## Installation

### Requirements

- **Python 3.8+**
- **PostgreSQL**

### Steps

1. **Clone the Repository**:

```bash  
   `git clone https://github.com/YOUR_USERNAME/API-ULOS-DB.git`  
   `cd API-ULOS-DB`
```
2. **Create and Activate a Virtual Environment**:

   - **Windows**:

```bash  
     `python -m venv env`  
     `.\\env\\Scripts\\activate`
```
   - **macOS/Linux**:

```bash  
     `python -m venv env`  
     `source env/bin/activate`
```
3. **Install Dependencies**:

```bash  
   `pip install -r requirements.txt`
```
4. **Configure the Database**:

   Create a `.env` file in the root folder with your database credentials:

```bash  
   `DATABASE_URL=postgres://username:password@localhost/ULOS_DB`
```
5. **Generate Database Schemas (First-Time Setup)**:

   When running the project for the first time, you'll need to create the database schema. In your `main.py` file, set `generate_schemas=True` in the Tortoise configuration:

   **Add Code Block Here (python)**  
   ```python
   from tortoise.contrib.fastapi import register_tortoise

   register_tortoise(
       app,
       db_url="postgres://username:password@localhost/ULOS_DB",
       modules={"models": ["app.models"]},
       generate_schemas=True  # Set to True for first-time setup
   )
```


---

## Running the Project

Start the FastAPI server:

```bash  
`uvicorn main:app --reload`
```
Visit the server at [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## API Endpoints

Here's a quick overview of the main endpoints:

| Method   | Endpoint                            | Description                       |
|----------|-------------------------------------|-----------------------------------|
| `POST`   | `/tasks/`                          | Create a new task                 |
| `GET`    | `/tasks/{task_id}`                 | Get a task by ID                  |
| `PUT`    | `/tasks/{task_id}`                 | Update a task                     |
| `DELETE` | `/tasks/{task_id}`                 | Delete a task                     |
| `PATCH`  | `/tasks/{task_id}/parsed_status`   | Update parsed status              |
| `PATCH`  | `/tasks/{task_id}/executed_status` | Update executed status            |
| `PATCH`  | `/tasks/{task_id}/state`           | Update state                      |

---

## Swagger UI

FastAPI provides an interactive Swagger UI to test the endpoints:

- Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for Swagger UI.
- Visit [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) for ReDoc.

---

## Screenshots

!!!Screenshots of your Swagger UI 

## Database Models

[View All Models in `models.py`](models.py)

## Contributing

Carlos German Monroy Andrade
201728260
Universidad de los Andes

### Steps to Contribute

1. Fork the repository.
2. Create a new branch:

```bash  
   `git checkout -b feature/your-feature-name`
```
3. Commit your changes:

```bash  
   `git commit -m "Add your feature"`
```
4. Push to the branch:

```bash 
   `git push origin feature/your-feature-name`
```
5. Open a Pull Request.

