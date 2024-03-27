# Projoint Django Project

Projoint is a Django-based project that provides a robust platform for managing projects and collaborations. This README file includes instructions on how to set up the project, create a superuser, and use the API endpoints.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python (>=3.6)
- Pip (package installer for Python)

## Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/aaronrkaufman/projointdesigntool.git
cd projoint
```

2. Create a virtual environment:

```bash
python3 -m venv venv
```

3. Activate the virtual environment (for Linux/macOS):

```bash
source venv/bin/activate
```

4. Install project dependencies:

```bash
pip install -r requirements.txt
```

5. Apply database migrations:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

## Update Requirements

If you have added any new libraries, run this command to update the requirements specifications

```bash
pip freeze > requirements.txt
```

## Create a Superuser

To create a superuser for accessing the Django admin interface and managing the application:

```bash
python manage.py createsuperuser
```

Follow the prompts to enter your desired username, email address, and password.

## Running the Development Server

To run the development server and access the API and admin interface, use the following command:

```bash
python3 manage.py runserver
```

## API Documentation

Documentation exists at

```
http://127.0.0.1:8000/api/swagger-ui/
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

## Markdown Pages

To load the pages

```bash
python3 manage.py loaddata markdown_pages.json
```

To upload the pages

```bash
python3 manage.py dumpdata dmd_app.MarkdownContent > markdown_pages.json
git add markdown_pages.json
git commit -m "docs: Add markdown pages data"
git push
```
