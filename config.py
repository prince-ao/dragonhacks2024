from decouple import config


class DevConfig:
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///lecture.db'
    DEBUG = True