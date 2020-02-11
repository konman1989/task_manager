from flask import request
from flask_restful import Resource
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError

from models import User, Event, serialize_multiple, user_subscriptions, \
    dashboard_users, task_users
from utils.validator import ModelValidator
from settings import db


class Events(Resource):

    def get(self):
        return ModelValidator(Event).get()

    def post(self):
        data = request.get_json()
        try:
            event = Event(**data)
            db.session.add(event)
            db.session.flush()
            id_ = event.id
            db.session.commit()
            return {"id": id_}, 201
        except TypeError:
            return "Wrong input", 400
        except IntegrityError:
            return "Either data already exists or wrong input", 409


class UserSubscriptions(Resource):

    def get(self, user_id):
        user = User.query.get(user_id)
        try:
            return serialize_multiple(user.subscriptions), 200
        except AttributeError:
            return "Not Found", 404

    def post(self, user_id):
        data = request.get_json()

        event_exists = Event.query.join(User, Event.subscribers).filter(
            and_(Event.event == data.get('event'),
                 User.chat_id == user_id)).first()

        if event_exists:
            return 'Already subscribed', 409

        try:
            event = db.session.query(Event).filter_by(
                event=data.get('event')).first()
            event.subscribers.append(User.query.get(user_id))

            db.session.commit()
            return {}, 201
        except AttributeError:
            return 'Wrong input', 422
        except FlushError:
            return 'Not registered', 403

    def delete(self, user_id):
        data = request.get_json()

        statement = user_subscriptions.delete().where(
            and_(user_subscriptions.columns.user_id == user_id,
                 user_subscriptions.columns.event == data.get(
                     'event')))

        db.session.execute(statement)
        db.session.commit()
        return {}, 200


class EventSubscribers(Resource):
    """Returns a list of users subscribed to given event. Filters by dashboard
    id (notifications about tasks) or task id (notifications about comments)"""

    def get(self, id_):
        args = request.args.get('query')
        if args == 'tasks':
            users = db.session.query(User).join(
                dashboard_users).filter(and_(
                dashboard_users.columns.dashboard_id == id_,
                user_subscriptions.columns.event == args,
                user_subscriptions.columns.user_id == dashboard_users.columns.user_id)
            )

            return serialize_multiple(users.all())

        if args == 'comments':
            users = db.session.query(User).join(
                task_users).filter(and_(
                task_users.columns.task_id == id_,
                user_subscriptions.columns.event == args,
                user_subscriptions.columns.user_id == task_users.columns.user_id)
            )

            return serialize_multiple(users.all())
