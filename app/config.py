import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL','postgresql://postgres:admin@localhost/modelado') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '123456'



