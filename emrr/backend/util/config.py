import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://emretainer:6yXgr68t3n.vB3gN@localhost/EMRetainer'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
