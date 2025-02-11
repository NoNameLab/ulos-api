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
   git clone https://github.com/YOUR_USERNAME/ulos-api.git
   cd ulos-api
   ```

2. **Create and Activate a Virtual Environment**:

   - **Windows**:

     ```bash
     python -m venv .venv
     .\.venv\Scripts\activate
     ```

   - **macOS/Linux**:

     ```bash
     python -m venv .venv
     source .venv/bin/activate
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

   Then, open the .env file and update all the neccesary fields

5. **Generate Database Schemas (First-Time Setup)**:

   The database schema will be generated automatically during the first run of the project. This process is managed by the `register_tortoise` function in `app/main.py`. Ensure that the `generate_schemas` flag is set to True before the first run.

   In the `app/main.py` file, set the `generate_schemas` parameter to True in the register_tortoise function:

   ```python
   try:
      register_tortoise(
         app,
         config=TORTOISE_ORM,
         add_exception_handlers=True,
         generate_schemas=True  # Set to True for first-time setup
      )
   except db_exception.ConfigurationError as e:
      print(f"An error has ocurred while configuring the database: {e}")
      raise e
   except db_exception.DBConnectionError as e:
      print(f"An error has ocurred while connecting to the database: {e}")
      raise e
   ```

   After running the project for the first time, set `generate_schemas` to `False` to avoid creating duplicate entries in the database:

   ```python
   try:
      register_tortoise(
         app,
         config=TORTOISE_ORM,
         add_exception_handlers=True,
         generate_schemas=False  # Set to False after initial setup
      )
   except db_exception.ConfigurationError as e:
      print(f"An error has ocurred while configuring the database: {e}")
      raise e
   except db_exception.DBConnectionError as e:
      print(f"An error has ocurred while connecting to the database: {e}")
      raise e
   ```

---

## Running the Project

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Visit the server at [http://127.0.0.1:8000](http://127.0.0.1:8000).

> **Note**: If you're running the project for the first time, ensure that `generate_schemas=True` in `app/config/database.py`. After the initial run, change it to `False` to prevent duplicate entries.

---

## API Endpoints

Here's a quick overview of the main endpoints:

| Method   | Endpoint                               | Description                                                                                                                                                                                                                                                                              |
| -------- | -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `POST`   | `/task-definitions`                    | Create a task definition and select the processing stages to include. It also uploads the image file from the container to the FTP server for each selected stage.                                                                                                                       |
| `GET`    | `/task-definitions`                    | Retrieves the list of created task definitions, along with their stages and the image file of the container.                                                                                                                                                                             |
| `PUT`    | `/task-definitions/{taskDefinitionId}` | Modify the details of a task definition, including its name, description, and associated processing stages.                                                                                                                                                                              |
| `DELETE` | `/task-definitions/{taskDefinitionId}` | Delete a specific task definition from the system.                                                                                                                                                                                                                                       |
| `GET`    | `/users/me/courses`                    | Retrieves the list of courses of a user. If the user is a professor, the courses they teach are returned. If the user is a student, the courses they are enrolled in are returned.                                                                                                       |
| `POST`   | `/courses/{courseId}/assignments`      | Create a new assignment for a specific course.                                                                                                                                                                                                                                           |
| `GET`    | `/courses/{courseId}/assignments/`     | Get all assignments created for a course, including the assignment name, task type, and due date.                                                                                                                                                                                        |
| `PUT`    | `/assignments/{assignmentId}`          | Modify the details of an assignment, such as its name, start date, and end date.                                                                                                                                                                                                         |
| `DELETE` | `/assignments/{assignmentId}`          | Delete a specific assignment of a course.                                                                                                                                                                                                                                                |
| `GET`    | `/assignments/{assignmentId}/tasks`    | Get students' submissions for a specific assignment, including the status of the parsing and execution stages.                                                                                                                                                                           |
| `GET`    | `/courses/{courseId}/assignments`      | Get all the assignments for a specific course and, if they have made a submission, view the parsing and execution statuses.                                                                                                                                                              |
| `POST`   | `/assignments/{assignmentId}/submit`   | Submits a task for a specific assignment. The submission is registered in the system, associating it with the user, the assignment, and the corresponding task definition. It uploads the corresponding file to the FTP server and publishes a message in the queue of the orchestrator. |
| `GET`    | `/assignments/{assignmentId}`          | Get the submission details for a specific assignment, including processing and status logs.                                                                                                                                                                                              |
| `POST`   | `/tasks/{taskId}/logs`                 | Adds a new log entry to the task_log table for a specific task.                                                                                                                                                                                                                          |
| `PATCH`  | `/tasks/{taskId}/requeue`              | Increases the requeue count of a task in the task_metrics table.                                                                                                                                                                                                                         |
| `PATCH`  | `/tasks/{taskId}`                      | Updates one or multiple statuses (e.g., parsing status, execution status) in the task_stage_status table.                                                                                                                                                                                |
| `GET`    | `/tasks`                               | Retrieves a list of all tasks stored in the system.                                                                                                                                                                                                                                      |
| `GET`    | `/tasks/{taskId}`                      | Retrieves detailed information about a specific task.                                                                                                                                                                                                                                    |
| `POST`   | `/auth/register`                       | Creates a new user account in the system.                                                                                                                                                                                                                                                |
| `POST`   | `/auth/login`                          | Authenticates a user and returns an access token for session management.                                                                                                                                                                                                                 |

---
