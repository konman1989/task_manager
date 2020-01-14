from flask import request
from flask_restful import Resource

from models import User, DashBoard, Task, serialize_multiple
from settings import db


class UserDashboards(Resource):

    def get(self, user_id):
        user = User.query.get(user_id)
        return serialize_multiple(user.dashboards)

    def post(self, user_id):
        data = request.get_json()

        d = DashBoard(admin=user_id, **data)

        db.session.add(d)
        db.session.flush()
        d.users.append(User.query.get(user_id))
        id_ = d.id
        db.session.commit()

        return {"id": id_}, 201


class UserDashboardsDetailed(Resource):

    def post(self, user_id, dashboard_id):
        data = request.get_json()
        d = DashBoard.query.get(dashboard_id)
        user = User.query.get(data.get('team'))

        if d.admin == user_id:
            d.users.append(user)
            db.session.commit()
            return {}, 201
        return "Only admins can add users to dashboard", 409

    def patch(self, user_id, dashboard_id):
        data = request.get_json()

        d = db.session.query(DashBoard).filter_by(id=dashboard_id)
        if d.first().admin == user_id:
            d.update(data)
            db.session.commit()
            return {}, 204
        return "Only admins can change dashboards", 409

    def delete(self, user_id, dashboard_id):
        d = db.session.query(DashBoard).filter_by(id=dashboard_id)
        if d.first().admin == user_id:
            d.delete()
            db.session.commit()
            return {}, 200
        return "Only admins can delete dashboards", 409


class UserTasks(Resource):

    def get(self, user_id, dashboard_id):
        user = User.query.get(user_id)

        return serialize_multiple([u for u in user.tasks if
                                   u.dashboard_id == dashboard_id]), 200

    def post(self, user_id, dashboard_id):
        data = request.get_json()
        d = DashBoard.query.get(dashboard_id)
        member = False

        for u in d.users:
            if u.id == user_id:
                member = True

        if member:
            task = Task(admin_id=user_id, dashboard_id=dashboard_id, **data)
            db.session.add(task)
            db.session.flush()
            id_ = task.id
            db.session.commit()

            return {"id": id_}, 201
        return "Only dashboard members can operate tasks", 409


