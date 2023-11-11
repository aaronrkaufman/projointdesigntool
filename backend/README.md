# Projoint Django Project

Projoint is a Django-based project that provides a robust platform for managing projects and collaborations. This README file includes instructions on how to set up the project, create a superuser, and use the API endpoints.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python (>=3.6)
- Pip (package installer for Python)

## Installation

1. Clone the repository to your local machine:

```
git clone https://github.com/aaronrkaufman/projointdesigntool.git
cd projoint
```

2. Create a virtual environment:

```
python3 -m venv venv
```

3. Activate the virtual environment (for Linux/macOS):

```
source venv/bin/activate
```

4. Install project dependencies:

```
pip install -r requirements.txt
```

5. Apply database migrations:

```
python3 manage.py makemigrations
python3 manage.py migrate
```

## Create a Superuser

To create a superuser for accessing the Django admin interface and managing the application:

```
python manage.py createsuperuser
```

Follow the prompts to enter your desired username, email address, and password.

## Running the Development Server

To run the development server and access the API and admin interface, use the following command:

```bash
python3 manage.py runserver
```

## API Documentation

### User Registration

Register a new user:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpassword", "email": "test@example.com"}' http://localhost:8000/api/profiles/register/
```

### User Login

Log in with existing user credentials:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpassword"}' http://localhost:8000/api/profiles/login/
```

It returns `token` on successful login.

### User Logout

Log out a user using their authentication token:

```bash
curl -X POST -H "Authorization: Token YOUR_AUTH_TOKEN" http://localhost:8000/api/profiles/logout/
```

## Testing APIs

To test specific command, run the module name of the API

```bash
python3 manage.py test $module
```

for example

```bash
python3 manage.py test surveys
```
