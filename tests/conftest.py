import pytest

from main import app
from models import User, DashBoard, Task
from settings import db


@pytest.fixture(scope='module')
def init_database():
    flask_app = app

    with flask_app.app_context():
        # Insert user data
        user1 = User(chat_id=12345,
                     username='Constantine',
                     email='constantine@gmail.com')
        user2 = User(chat_id=678910,
                     username='Steve',
                     email='steve@gmail.com')

        user3 = User(chat_id=54321,
                     username='John',
                     email='john@gmail.com')

        dashboard = DashBoard(id=55555,
                              admin=12345,
                              dashboard_name='Flask')

        dashboard.users.append(user1)
        dashboard.users.append(user3)

        task = Task(id=66666,
                    admin=12345,
                    task_name='Run tests',
                    text="Use Pytest",
                    dashboard_id=55555)

        db.session.add(user1)
        db.session.add(user2)
        db.session.add(dashboard)
        db.session.add(task)
        db.session.commit()

        yield flask_app

        db.session.query(User).delete()
        # db.session.query(Dashboard).delete()
        db.session.commit()


@pytest.fixture(scope='module')
def test_client():
    flask_app = app
    # flask_app.testing = True
    flask_app.config['TESTING'] = True
    # Flask provides a way to test your application by exposing
    # the Werkzeug test Client and handling the context locals for you.
    testing_client = flask_app.test_client()
    # Establish an application context before running the tests.

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()
