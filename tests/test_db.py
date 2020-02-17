import os
import pytest
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f'postgresql://konstantin:' \
                                 f'{POSTGRES_PASSWORD}@localhost/test_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)


@pytest.fixture(scope='module')
def test_client():
    # flask_app = app
    #
    # # Flask provides a way to test your application by exposing
    # # the Werkzeug test Client and handling the context locals for you.
    # testing_client = flask_app.test_client()
    #
    # # Establish an application context before running the tests.
    # ctx = flask_app.app_context()
    # ctx.push()
    #
    # yield testing_client  # this is where the testing happens!
    #
    # ctx.pop()
    flask_app = app


    with flask_app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()



@pytest.fixture(scope='module')
def init_database():
    pass


def test_get(test_client):
    response = test_client.get('/users')

    assert response.status_code == 200
    assert b'Constantine' in response.data



