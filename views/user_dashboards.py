from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError, InvalidRequestError

from models import User, DashBoard, Task, serialize_multiple
from settings import db


class UserDashboards(Resource):

    def get(self, user_id):
        try:
            user = User.query.get(user_id)
            return serialize_multiple(user.dashboards), 200
        except AttributeError:
            return "Not found", 404

    def post(self, user_id):
        try:
            data = request.get_json()

            d = DashBoard(admin=user_id, **data)

            db.session.add(d)
            db.session.flush()
            d.users.append(User.query.get(user_id))
            id_ = d.id
            db.session.commit()
            return {"id": id_}, 201
        except TypeError:
            return "Wrong input", 400
        except IntegrityError:
            return "Either data already exists or wrong input", 409


class UserDashboardsDetailed(Resource):

    def post(self, user_id, dashboard_id):
        data = request.get_json()

        d = DashBoard.query.get(dashboard_id)
        user = User.query.get(data.get('team'))

        if user is None or d is None:
            return "Wrong input", 400

        if d.admin == user_id:
            d.users.append(user)
            db.session.commit()
            return {}, 201
        return "Only admins can add users to dashboard", 409

    def patch(self, user_id, dashboard_id):
        data = request.get_json()

        try:
            d = db.session.query(DashBoard).filter_by(id=dashboard_id)
            if d.first().admin == user_id:
                d.update(data)
                db.session.commit()
                return {}, 204
            return "Only admins can change dashboards", 409
        except InvalidRequestError:
            return 'Wrong input', 400
        except AttributeError:
            return 'Not found', 404

    def delete(self, user_id, dashboard_id):
        try:
            d = db.session.query(DashBoard).filter_by(id=dashboard_id)
            if d.first().admin == user_id:
                d.delete()
                db.session.commit()
                return {}, 200
            return "Only admins can delete dashboards", 409
        except AttributeError:
            return 'Not found', 404

