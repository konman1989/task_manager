from flask import request
from flask_restful import Resource

from models import User, Task, Comment
from settings import db


class UserTasksDetailed(Resource):

    def get(self, user_id, dashboard_id, task_id):
        task = Task.query.get(task_id)

        if task.dashboard_id == dashboard_id:
            for user in task.users:
                if user.id == user_id:
                    return task.serialize(), 200
        return "Either access is restricted or wrong dashboard", 409

    def post(self, user_id, dashboard_id, task_id):
        data = request.get_json()
        task = Task.query.get(task_id)
        user = User.query.get(data.get('team'))

        if task.dashboard_id == dashboard_id and task.admin_id == user_id:
            task.users.append(user)
            db.session.commit()
            return {}, 201
        return "Either access is restricted or wrong dashboard", 409

    def patch(self, user_id, dashboard_id, task_id):
        data = request.get_json()
        task = db.session.query(Task).filter_by(id=task_id)
        if data.get('admin_id') != task.first().admin_id \
                and task.first().admin_id != user_id:
            return "Only admins can change tasks admin", 409
        if task.first().dashboard_id != dashboard_id:
            return "Wrong dashboard", 409
        task.update(data)
        db.session.commit()
        return {}, 204


class UserTaskComments(Resource):

    def get(self, user_id, dashboard_id, task_id):
        task = Task.query.get(task_id)

        if task.dashboard_id == dashboard_id:
            for user in task.users:
                if user.id == user_id:
                    return [t.serialize() for t in task.comments], 200

        return "Either access is restricted or wrong dashboard", 409

    def post(self, user_id, dashboard_id, task_id):
        data = request.get_json()
        task = Task.query.get(task_id)

        if task.dashboard_id == dashboard_id:
            for user in task.users:
                if user.id == user_id:
                    c = Comment(sender_id=user_id, task_id=task_id, **data)
                    db.session.add(c)
                    db.session.flush()
                    id_ = c.id
                    db.session.commit()

                    return {'id': id_}, 200
        return "Either access is restricted or wrong dashboard", 409
