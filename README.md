# Smart Library Management System

## Project Overview
The Smart Library Management System is a web-based application developed using Python and Flask to manage library books, users, borrowing, and returns. The application is containerized using Docker and deployed on an AWS EC2 Ubuntu instance.

## Technologies Used
- Python
- Flask
- HTML and CSS
- Docker
- AWS EC2 (Ubuntu)
- Git and GitHub
- Pytest for automated testing

## Features
- Display available library books
- Manage library users
- Borrow books and process returns
- Provide API endpoints for library operations
- Run the application inside a Docker container
- Test core functionality using automated tests

## Project Structure
- `app/` — application routes, models, services, and templates
- `database/` — database-related code
- `tests/` — automated tests
- `Dockerfile` — Docker image instructions
- `requirements.txt` — Python dependencies
- `run.py` — application entry point
- `k8s/` — Kubernetes configuration files

## Run Locally
1. Install Python and Docker.
2. Install the Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the application:

   ```bash
   python run.py
   ```

Use the host and port configured by the application to access it in your browser.

## Run with Docker
Build the image:

```bash
docker build -t smart-library:1.4 .
```

Run the container:

```bash
docker run -d --name smart-library -p 5000:5000 smart-library:1.4
```

Open `http://localhost:5000` in your browser.

## Testing
Run the automated tests with:

```bash
pytest
```

## Deployment
The application has been deployed on an AWS EC2 Ubuntu instance using Docker. Configure the required AWS security-group rules before accessing the application remotely.

## Note
The application currently uses in-memory data for some library operations. Data may reset when the application restarts.
