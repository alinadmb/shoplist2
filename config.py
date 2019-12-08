import os
from dotenv import load_dotenv
import psycopg2

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #                            'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = 'postgres://hasszyqlmsllov:a4b06cdf239afa543a717b10e0bf496c5328dfcdde36d5d942b2f08acf079e23@ec2-174-129-255-39.compute-1.amazonaws.com:5432/dfjbumi1kkkj2u'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    # STATICFILES_DIRS = (os.path.join(basedir, "static"))