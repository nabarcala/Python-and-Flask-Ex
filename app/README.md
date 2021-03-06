# Python-and-Flask-Ex
Some notes from building the web application.

## Virtual Environment
Start by installing Flask in a virtual environmnet, e.g. virtualenv. This can be downloaded from [https://pypi.python.org/pypi/virtualenv](https://pypi.python.org/pypi/virtualenv).

I created a directory for this project (e.g. python-flask-ex) and created and activated a virtual environment called flask_venv.
```
python3 -m venv flask_venv
virtualenv flask_venv
source flask_venv/Scripts/activate
```

Then install all the required packages from requirements.txt like so:
```
pip install -r requirements.txt
```

## Web Application
The application can be called from [portfolio.py](portfolio.py). This file calls the flask application instance called portfolio that is located in the app package. Set the FLASK_APP environment variable so Flask knows what to import. This is done in the [.flaskenv](.flaskenv) file like so:
```
export FLASK_APP=app.py
```
The application can then be run using:
```
flask run
```

## Database
SQLAlchemy is a Python SQL toolkit and Object Relational Mapper that allows this application the full power and flexibility of SQL. The application's database is located at the base directory in a file called app.db. This file, along with the migration folder, can be created by running the following commands:
```
flask db init
flask db migrate -m "Initial tables"
flask db upgrade
```
Where -m is the message flag for the comment "Initial tables".

## Some Cool Tools Used
JQuery:
* [Font Awesome](https://fontawesome.com/v4.7.0/): The iconic font and CSS toolkit.
* [Boxicons](https://boxicons.com/): Simple vector icons set carefully crafted for designers and developers to use in your next project
* [fancyBox](https://fancyapps.com/fancybox/): A tool that offers a nice and elegant way to add zooming functionality for images, html content and multi-media on your webpages.
* [Slick Slider](https://kenwheeler.github.io/slick/): A responsive carousel jQuery plugin.