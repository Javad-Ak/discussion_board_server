# Discussion Board Server: django restful API

## Description

Discussion Board is a simple django restful API with user authentication and discussion management.
Documentation is available at /api/docs/.

## Quick Start

Build a local python venv and install dependencies using pip:

```
pip install -r requirements.txt
```

Build local sqlite database and run the server:

```
python manage.py makemigrations accounts discussions
python manage.py migrate
python manage.py runserver
```

Note that the port is localhost:8000 and DEBUG is True.