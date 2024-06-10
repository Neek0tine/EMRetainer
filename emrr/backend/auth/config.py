import secrets

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://emretainer:6yXgr68t3n.vB3gN@localhost/EMRetainer'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.token_hex()
