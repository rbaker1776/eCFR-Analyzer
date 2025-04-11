import os


class Config:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"


class DevConfig(Config):
    DEBUG = True
