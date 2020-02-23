# Python-and-Flask-Ex
Simple and to the point Python and Flask microservice practice.

## Virtual Environment
Start by installing Flask in a virtual environmnet, e.g. virtualenv. This can be downloaded from [https://pypi.python.org/pypi/virtualenv](https://pypi.python.org/pypi/virtualenv).

I created a directory for this project (e.g. python-flask-ex) and created and activated a virtual environment called venv.
```
virtualenv venv
. venv/bin/activate
```

The simplest way to install Flask:
```
pip install flask
```

## Web Application
The application is located in the app folder and can be called from [app.py](app.py). This file calls the flask application instance called app that is located in the app package. Set the FLASK_APP environment variable so Flask knows what to import.
```
export FLASK_APP=app.py
```
The application can then be run using:
```
flask run
```

## Database Models
Flask-Migrate contains a framework called Alembic that can make changes to schemas of the database structure but does not require the database to be recreated. Alembic uses a migration repository by creating a directory to hold migration scripts that keep track of all the changes that have taken place. To create this migration repository, run:
```
flask db init
```

Flask-Migrate exposes its commands through the flask command. You have already seen flask run, which is a sub-command that is native to Flask. The flask db sub-command is added by Flask-Migrate to manage everything related to database migrations. So let's create the migration repository for microblog by running flask db init:
