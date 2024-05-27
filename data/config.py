# -- coding: utf-8 --
from dataclasses import dataclass
from os import path, getenv

from dotenv import load_dotenv

env_path = 'data/.env'
if not path.exists(env_path):
    print(f'\033[1m\033[31m[ERROR]\033[0m File with environment variable data NOT found. env_path: "{env_path}"')
    exit()
load_dotenv(env_path)


@dataclass
class Config:
    SECRET_KEY: str = getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    FLASK_PORT: int = getenv('FLASK_PORT')

    db_type: str = getenv('DB_TYPE', 'MySQLDatabase')
    db_name: str = getenv('DB_NAME')
    db_user: str = getenv('DB_USER')
    db_password: str = getenv('DB_PASSWORD')
    db_host: str = getenv('DB_HOST')
    db_port: int = int(getenv('DB_PORT', 3306))

    SQLALCHEMY_DATABASE_URI: str = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

    default_roles = ['admin', 'manager', 'analyst', 'customer1', 'customer2', 'customer3']


config = Config()
