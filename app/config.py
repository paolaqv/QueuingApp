import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL','postgresql://postgres:marceline25@localhost/modelado') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '123456'



