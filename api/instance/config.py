import os
from dotenv import load_dotenv
load_dotenv()


class BaseConfig(object):
    """A configuration template class that is overridden by other classes"""
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    DATABASE_USER = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DEBUG = False
    TESTING = False
    JWT_SECRET_KEY = os.getenv("SECRET_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")
    DATABASE_HOST = os.getenv("DATABASE_HOST")


class DevConfig(BaseConfig):
    """Configuration for development environment"""
    DEBUG = True


class TestingConfig(DevConfig):
    """Configuration for Testing application in tests"""
    TESTING = True
    DATABASE_NAME = os.getenv("TEST_DABASE")


app_config = {
    "TESTING": TestingConfig,
    "DEVELOPMENT": DevConfig
}
