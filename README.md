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
