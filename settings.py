import logging
import os

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_URL = os.getenv('POSTGRES_URL')

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:' \
                                 f'{POSTGRES_PASSWORD}@{POSTGRES_URL}/postgres'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
