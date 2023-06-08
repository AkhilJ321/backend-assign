# User Management System

This is a simple User Task Management System REST API built using Python and Flask. It provides endpoints to create, update, list, and paginate tasks.

## Prerequisites

- Python 3.7 or higher
- Flask
- Flask SQLAlchemy

## Getting Started

1. **Clone the repository:**

   ```bash
   git clone https://github.com/AkhilJ321/backend-assign.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd backend-assign
   ```

3. **Create and activate a virtual environment (optional):**

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

4. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Start the Flask development server:**

   ```bash
   flask run
   ```

6. **Open your web browser and access the following URL:**

   ```
   http://localhost:5000
   ```

7. **Use an API testing tool like Postman to interact with the API endpoints:**

   - **Create a task:** Send a POST request to `/tasks` with the task details in the request body.
   - **Receive a single task:** Send a POSTS request to `/tasks{task_id}`.

   - **Update a task:** Send a PUT request to `/tasks/{task_id}` with the updated task details in the request body.

   - **List all tasks:** Send a GET request to `/tasks`.

     - Optional query parameters:
       - `page` (default: 1): The page number for pagination.
       - `per_page` (default: 10): The number of tasks to display per page.

8. **Explore the API endpoints and test different requests based on your requirements.**

## Project Structure

- `app.py`: The main Flask application file containing the API endpoints and configurations.
- `requirements.txt`: Lists the required Python packages and their versions.
- `README.md`: Project documentation file.


