import os
from dotenv import load_dotenv


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', "most-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        "sqlite:///" + os.path.join(BASE_DIR, "devdb.db")
    FLASK_ENV = 'development'


class TestingCongig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        "sqlite:///"
    TESTING = True


config_class = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'testing': TestingCongig
}
