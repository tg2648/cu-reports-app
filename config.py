"""
Application configuration
"""

# Standard library imports
import os

# Third party imports
import boto3
from dotenv import load_dotenv
from itsdangerous.url_safe import URLSafeSerializer


basedir = os.path.abspath(os.path.dirname(__file__))  # This directory
load_dotenv(os.path.join(basedir, '.env'))  # Add .env to environment variables


class Config(object):
    """Base configuration"""

    SECRET_KEY = os.getenv('SECRET_KEY')
    SERIALIZER = URLSafeSerializer(SECRET_KEY)
    SESSION_COOKIE_SECURE = True

    # CAS
    CAS_LOGIN_ROUTE = os.getenv('CAS_LOGIN_ROUTE')
    CAS_LOGOUT_ROUTE = os.getenv('CAS_LOGOUT_ROUTE')
    CAS_VALIDATE_ROUTE = os.getenv('CAS_VALIDATE_ROUTE')
    CAS_AFTER_LOGIN = os.getenv('CAS_AFTER_LOGIN')

    # Dynamo [required by flask_dynamo]
    DYNAMO_SESSION = boto3.Session(
        region_name='us-east-2',
        aws_access_key_id=os.getenv('DB_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('DB_SECRET')
    )

    # S3
    S3_RESOURCE = boto3.resource(
        's3',
        aws_access_key_id=os.getenv('S3_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('S3_SECRET')
    )
    FIF_FILES_BUCKET = os.getenv('FIF_BUCKET_NAME')
    TEMPLATES_BUCKET = os.getenv('TEMPLATES_BUCKET_NAME')

    FORM_URL = os.getenv('FORM_URL')


class ProdConfig(Config):
    """Production configuration"""

    ENV = 'prod'
    DEBUG = False

    CAS_SERVER = os.getenv('CAS_SERVER_PROD')
    CAS_AFTER_LOGOUT = os.getenv('CAS_AFTER_LOGOUT_PROD')
    DB_USERS = os.getenv('DB_USERS_PROD')
    DB_ACCESS_LOGS = os.getenv('DB_ACCESS_LOGS_PROD')
    DB_SEARCHCOM_APPLICANT = os.getenv('DB_SEARCHCOM_APPLICANT_PROD')
    DB_SEARCHCOM_POSTING = os.getenv('DB_SEARCHCOM_POSTING_PROD')
    DB_SEARCHCOM_PIPELINE = os.getenv('DB_SEARCHCOM_PIPELINE_PROD')
    DB_SEARCHCOM_SUBFIELDS = os.getenv('DB_SEARCHCOM_SUBFIELDS_PROD')
    DB_LAB_OCCUPANCY = os.getenv('DB_LAB_OCCUPANCY_PROD')
    DB_DEPTPROFILE = os.getenv('DB_DEPTPROFILE_PROD')
    DB_REPOSITORY = os.getenv('DB_REPOSITORY_PROD')
    REPOSITORY_BUCKET = os.getenv('REPOSITORY_BUCKET_NAME_PROD')


class DevConfig(Config):
    """Development configuration"""

    ENV = 'dev'
    DEBUG = True

    CAS_SERVER = os.getenv('CAS_SERVER_DEV')
    CAS_AFTER_LOGOUT = os.getenv('CAS_AFTER_LOGOUT_DEV')
    DB_USERS = os.getenv('DB_USERS_DEV')
    DB_ACCESS_LOGS = os.getenv('DB_ACCESS_LOGS_DEV')
    DB_SEARCHCOM_APPLICANT = os.getenv('DB_SEARCHCOM_APPLICANT_DEV')
    DB_SEARCHCOM_POSTING = os.getenv('DB_SEARCHCOM_POSTING_DEV')
    DB_SEARCHCOM_PIPELINE = os.getenv('DB_SEARCHCOM_PIPELINE_DEV')
    DB_SEARCHCOM_SUBFIELDS = os.getenv('DB_SEARCHCOM_SUBFIELDS_DEV')
    DB_LAB_OCCUPANCY = os.getenv('DB_LAB_OCCUPANCY_DEV')
    DB_DEPTPROFILE = os.getenv('DB_DEPTPROFILE_DEV')
    DB_REPOSITORY = os.getenv('DB_REPOSITORY_DEV')
    REPOSITORY_BUCKET = os.getenv('REPOSITORY_BUCKET_NAME_DEV')
