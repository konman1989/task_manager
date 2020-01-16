from flask import request
from flask_restful import Resource

from models import User, DashBoard, Task, Comment, serialize_multiple
from settings import db


class UserTasks(Resource):

    def get(self, user_id, dashboard_id):
        user = User.query.get(user_id)
        try:
            return serialize_multiple([u for u in user.tasks if
                                       u.dashboard_id == dashboard_id]), 200
        except AttributeError:
            return 'Not found', 404

    def post(self, user_id, dashboard_id):
        """Creates new task. Checks if a dashboard member"""

        data = request.get_json()
        d = DashBoard.query.get(dashboard_id)

        if d is None:
            return 'Wrong input', 400
        member = False

        for u in d.users:
            if u.id == user_id:
                member = True
                break

        if member:
            try:
                task = Task(admin_id=user_id,
                            dashboard_id=dashboard_id,
                            **data)
                db.session.add(task)
                db.session.flush()
                id_ = task.id
                db.session.commit()
                return {"id": id_}, 201
            except TypeError:
                return 'Wrong input', 400
        return "Only dashboard members can operate tasks", 409


class UserTasksDetailed(Resource):

    def get(self, user_id, dashboard_id, task_id):
        task = Task.query.get(task_id)
        d = DashBoard.query.get(dashboard_id)
        member = False

        for u in d.users:
            if u.id == user_id:
                member = True
                break

        if task.dashboard_id == dashboard_id and member:
            return task.serialize(), 200
        return "Either access is restricted or wrong dashboard", 409

    def post(self, user_id, dashboard_id, task_id):
        """Adds a new user to the task. Checks if the initiator is admin"""

        data = request.get_json()
        task = Task.query.get(task_id)
        user = User.query.get(data.get('team'))

        if user is None or task is None:
            return "Wrong input", 400

        if task.dashboard_id == dashboard_id and task.admin_id == user_id:
            task.users.append(user)
            db.session.commit()
            return {}, 201
        return "Either access is restricted or wrong dashboard", 409

    def patch(self, user_id, dashboard_id, task_id):
        """Updates task details. Checks if the user is in the dashboard"""

        data = request.get_json()

        d = DashBoard.query.get(dashboard_id)
        member = False

        for user in d.users:
            if user.id == user_id:
                member = True
                break

        if member:
            try:
                task = db.session.query(Task).filter_by(id=task_id)
                if data.get('admin_id') is not None and \
                        task.first().admin_id != data.get('admin_id') \
                        and user_id != task.first().admin_id:
                    return "Only task admins can change admins", 409

                if task.first().dashboard_id != dashboard_id:
                    return "Wrong dashboard", 409
                task.update(data)
                db.session.commit()
                return {}, 204
            except AttributeError:
                return 'Not found', 404
        return 'Only dashboard members can manipulate tasks', 409


class UserTaskComments(Resource):

    def get(self, user_id, dashboard_id, task_id):
        task = Task.query.get(task_id)
        d = DashBoard.query.get(dashboard_id)
        member = False

        for user in d.users:
            if user.id == user_id:
                member = True
                break

        if member and task.dashboard_id == dashboard_id:
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
