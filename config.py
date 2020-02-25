import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # Using a SQLite database 
    # Take the location of the application's database from the SQLALCHEMY_DATABASE_URI configuration variable
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    # Disable the signal for everytime something changes in the database
    SQLALCHEMY_TRACK_MODIFICATIONS = False