import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # Using a SQLite database 
    # Take the location of the application's database from the SQLALCHEMY_DATABASE_URI configuration variable
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'port.db')
    # Disable the signal for everytime something changes in the database
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Heroku expects applications to log directly to stdout
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    
    # Email server details
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['nabarcala@gmail.com']
    
    POSTS_PER_PAGE = 25
    
    LANGUAGES = ['en', 'es']

    UPLOADS_DEFAULT_DEST = os.environ.get('UPLOADS_DEFAULT_DEST') or os.path.join(basedir, 'app/static/img')
    # images = UploadSet('images', IMAGES)
    # configure_uploads(images)
    