import os
basedir = os.path.abspath(os.path.dirname(__file__))

database_name = "qa4anything"
database_path = "postgres://{}/{}".format(
    'postgres:password321@localhost:5432', database_name)

class Config:
    # SECRET_KEY = os.environ.get("SECRET KEY")
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL")
    SQLALCHEMY_DATABASE_URI = database_path



class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = database_path


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}