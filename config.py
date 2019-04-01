import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
<<<<<<< HEAD
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
=======
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
>>>>>>> 366789dfea0067ca83a10c83a54d80a2155c4661
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
<<<<<<< HEAD
    ADMINS = os.environ.get('ADMINS')
=======
    ADMINS = ['textannotate@gmail.com']
>>>>>>> 366789dfea0067ca83a10c83a54d80a2155c4661
    