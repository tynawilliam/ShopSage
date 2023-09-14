import os
from decouple import config


class Config:
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = config('SECRET_KEY', default=os.urandom(24))
    JWT_SECRET_KEY = config('JWT_SECRET_KEY', default=os.urandom(24))
