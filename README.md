# ULOS API

The ULOS API is a FastAPI-based system designed to manage tasks, users, and execution logs, leveraging Tortoise ORM and PostgreSQL. It enables the efficient processing of various tasks, which are orchestrated by the Uniandes Lab Orchestration System [(ULOS)](https://github.com/est-gonzalezr/ulos). This API provides a set of CRUD operations, state management for tasks, and error logging, which are essential for interacting with ULOS.

The ULOS API is built to serve as the backend interface for faculty, students, and monitors of the Virtual Masters program at the Universidad de los Andes. It allows users to submit tasks, track their status in real-time, and retrieve detailed execution logs. Eventually, a web interface will be developed to interact with this API, streamlining the process of task management and monitoring for all users involved in the system.

---

## Table of Contents

1. [Installation](#installation)
2. [Running the Project](#running-the-project)
3. [API Endpoints](#api-endpoints)

---

## Installation

### Requirements

- **Python 3.8+**
- **PostgreSQL**

### Steps

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/YOUR_USERNAME/API-ULOS-DB.git
   cd API-ULOS-DB
   ```

2. **Create and Activate a Virtual Environment**:

   - **Windows**:

     ```bash
     python -m venv env
     .\env\Scripts\activate
     ```

   - **macOS/Linux**:

     ```bash
     python -m venv env
     source env/bin/activate
     ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Database**:

   Copy the `.env.example` file to `.env` and edit it to include your database credentials:

   ```bash
   cp .env.example .env
   ```

   Then, open the .env file and update the `DB_URL` with your PostgreSQL credentials:

   ```dotenv
   DB_URL=postgres://username:password@localhost/ULOS_DB
   ```

5. **Generate Database Schemas (First-Time Setup)**:

   The database schema will be generated automatically during the first run of the project. This process is managed by the `init_db` function in `app/config/database.py`. Ensure that the `generate_schemas` flag is set to True before the first run.

   In the `app/config/database.py` file, set the `generate_schemas` parameter to True in the register_tortoise function:

   ```python
   def init_db(app):
      register_tortoise(
         app,
         db_url=DB_URL,
         modules={"models": ["app.models"]},
         generate_schemas=True,  # Set to True for first-time setup
         add_exception_handlers=True,
      )
   ```

   After running the project for the first time, set `generate_schemas` to `False` to avoid creating duplicate entries in the database:

   ```python
   def init_db(app):
      register_tortoise(
         app,
         db_url=DB_URL,
         modules={"models": ["app.models"]},
         generate_schemas=False,  # Set to False after initial setup
         add_exception_handlers=True,
      )
   ```

---

## Running the Project

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Visit the server at [http://127.0.0.1:8000](http://127.0.0.1:8000).

> **Note**: If you're running the project for the first time, ensure that `generate_schemas=True` in `app/config/database.py`. After the initial run, change it to `False` to prevent duplicate entries.

---

## API Endpoints

Here's a quick overview of the main endpoints:

| Method   | Endpoint                           | Description            |
| -------- | ---------------------------------- | ---------------------- |
| `POST`   | `/tasks/`                          | Create a new task      |
| `GET`    | `/tasks/{task_id}`                 | Get a task by ID       |
| `PUT`    | `/tasks/{task_id}`                 | Update a task          |
| `DELETE` | `/tasks/{task_id}`                 | Delete a task          |
| `PATCH`  | `/tasks/{task_id}/parsed_status`   | Update parsed status   |
| `PATCH`  | `/tasks/{task_id}/executed_status` | Update executed status |
| `PATCH`  | `/tasks/{task_id}/state`           | Update state           |

---
