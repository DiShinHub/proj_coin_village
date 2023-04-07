import os
import datetime
import logging.config
import json

from dotenv import load_dotenv
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False

    # JWT Options
    JWT_TOKEN_LOCATION = 'headers'
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_IDENTITY_CLAIM = 'sub'
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ALGORITHM = "HS256"
    log_config = json.load(open(f'{basedir}/logger.json'))
    logging.config.dictConfig(log_config)



class DevelopmentConfig(Config):

    DEBUG = True
    PROPAGATE_EXCEPTIONS = True
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=365000)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=365000)

    # DB
    # pool_pre_ping : 데이터베이스 연결확인 핑
    # pool_recycle: 커넥션 오토 리사이클 주기 (sec)
    # pool_size: 커넥션 풀 사이즈
    # max_overflow : 최대 커넥션 풀 사이즈 이후 생성 가능 커넥션 수
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 1800,
        'pool_size': 5,
        'pool_timeout': 100,
        'pool_pre_ping': True,
        'max_overflow': 10
    }

    db = {
        'user': os.getenv("DB_USER"),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': 3306,
        'database': os.getenv('DB_DATABASE')
    }
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8mb4&collation=utf8mb4_unicode_ci&ssl_disabled=True"


class ProductionConfig(Config):
    
    PROPAGATE_EXCEPTIONS = True
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=365000)

    # DB
    # pool_pre_ping : 데이터베이스 연결확인 핑
    # pool_recycle: 커넥션 오토 리사이클 주기 (sec)
    # pool_size: 커넥션 풀 사이즈
    # max_overflow : 최대 커넥션 풀 사이즈 이후 생성 가능 커넥션 수
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 1800,
        'pool_size': 5,
        'pool_timeout': 100,
        'pool_pre_ping': True,
        'max_overflow': 10
    }

    db = {
        'user': os.getenv("DB_USER"),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': 3306,
        'database': os.getenv('DB_DATABASE')
    }
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8mb4&collation=utf8mb4_unicode_ci&ssl_disabled=True"

    # slave db
    db_slave = {
        'user': os.getenv("DB_SLAVE_USER"),
        'password': os.getenv('DB_SLAVE_PASSWROD'),
        'host': os.getenv('DB_SLAVE_HOST'),
        'port': 3306,
        'database': os.getenv('DB_SLAVE_DATABASE')
    }

    SQLALCHEMY_BINDS = {
        'master': SQLALCHEMY_DATABASE_URI,
        'slave': f"mysql+mysqlconnector://{db_slave['user']}:{db_slave['password']}@{db_slave['host']}:{db_slave['port']}/{db_slave['database']}?charset=utf8mb4&collation=utf8mb4_unicode_ci&ssl_disabled=True"
    }
    AUTO_READ_ON_SLAVE = True


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig,
)
