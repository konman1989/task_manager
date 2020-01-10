from flask import request
from flask_restful import Resource

from models import User
from utils.validator import ModelValidator
from settings import db


class Users(Resource):

    def get(self):
        return ModelValidator(User).get()

    def post(self):
        data = request.get_json()
        return ModelValidator(User).post(**data)


class SingleUser(Resource):

    def get(self, user_id):
        return ModelValidator(User).get_by_id(user_id)

    def patch(self, user_id):
        data = request.get_json()
        return ModelValidator(User).patch_by_id(user_id, data)

    def delete(self, user_id):
        db.session.query(User).filter_by(id=user_id).delete()
        db.session.commit()
        return {}, 200


class UserStats(Resource):

    def get(self, user_id):
        args = request.args.get('query')

        if args is not None:
            user = User.query.get(user_id)
            if args == 'dashboards':
                return [u.serialize() for u in user.dashboards], 200
            elif args == 'tasks':
                return [u.serialize() for u in user.tasks], 200
            elif args == 'comments':
                return [u.serialize() for u in user.comments], 200
        return {}, 200
