# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from decouple import config
import bleach

def uia_username_mapper(identity):
    # we allow pretty much anything - but we bleach it.
    return bleach.clean(identity, strip=True)

class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))

    # Set up the App SECRET_KEY
    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')

    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
    }

    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')

    SECURITY_CHANGEABLE = True
    SECURITY_POST_CHANGE_VIEW = "/login"
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False

    SECURITY_RECOVERABLE = True


    SECURITY_USER_IDENTITY_ATTRIBUTES = [
        {"username": {"mapper": uia_username_mapper}}
    ]
    
    FLASK_ADMIN_SWATCH = 'cerulean'

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = "webapptest2022@gmail.com"
    MAIL_PASSWORD = "webapp1234"
    
    UPLOAD_FOLDER = 'tmp'

    CKEDITOR_FILE_UPLOADER = 'prefall_blueprint.upload'
    # CKEDITOR_ENABLE_CSRF = True  # if you want to enable CSRF protect, uncomment this line
    UPLOADED_PATH = os.path.join(basedir, 'uploads')


class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config('DB_ENGINE', default='postgresql'),
        config('DB_USERNAME', default='appseed'),
        config('DB_PASS', default='pass'),
        config('DB_HOST', default='localhost'),
        config('DB_PORT', default=5432),
        config('DB_NAME', default='appseed-flask')
    )

    
    

class DebugConfig(Config):
    DEBUG = True

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        os.getenv('DB_ENGINE'),
        os.getenv('DB_USERNAME'),
        os.getenv('DB_PASS'),
        os.getenv('DB_HOST'),
        os.getenv('DB_PORT'),
        os.getenv('DB_NAME')
    )

    #SQLALCHEMY_DATABASE_URI = 'mysql://zAKPC936JP:UloEGPhfyS@remotemysql.com/zAKPC936JP'
    #SQLALCHEMY_DATABASE_URI = 'mysql://root:1234@localhost/webapp'
    #SQLALCHEMY_DATABASE_URI = 'mysql://webapp:webapp@localhost/prefall'

    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@srv.ibc.bio:32817/prefall'
    #SQLALCHEMY_DATABASE_URI = 'mysql://root:root@srv.ibc.bio:32817/prefall_prod'
    
# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}
