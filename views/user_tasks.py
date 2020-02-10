from flask import request
from flask_restful import Resource
from sqlalchemy import and_

from models import User, DashBoard, Task, Comment, serialize_multiple
from services import init_event_creation
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
        # checking if user_id in dashboard
        member = DashBoard.query.join(User, DashBoard.users).filter(
            and_(DashBoard.id == dashboard_id,
                 User.chat_id == user_id)).first()

        if member:
            try:
                task = Task(admin=user_id,
                            dashboard_id=dashboard_id,
                            **data)
                db.session.add(task)
                db.session.flush()
                task.users.append(User.query.get(user_id))
                id_ = task.id
                db.session.commit()

                # sending a new task notification
                init_event_creation('tasks', task.serialize())

                return {"id": id_}, 201
            except TypeError:
                return 'Wrong input', 400
        return "Either access is restricted or wrong dashboard", 409


class UserTasksDetailed(Resource):

    def get(self, user_id, dashboard_id, task_id):
        task = Task.query.get(task_id)
        # checking if user_id in dashboard
        member = DashBoard.query.join(User, DashBoard.users).filter(
            and_(DashBoard.id == dashboard_id,
                 User.chat_id == user_id)).first()

        try:
            if task.dashboard_id == dashboard_id and member:
                return task.serialize(), 200
            return "Either access is restricted or wrong dashboard", 409
        except AttributeError:
            return "Not Found", 404

    def post(self, user_id, dashboard_id, task_id):
        """Adds a new user to the task. Checks if the initiator is dashboard
        member"""

        data = request.get_json()
        task = Task.query.get(task_id)
        user = User.query.get(data.get('team'))

        if user is None or task is None:
            return "Wrong input", 400

        # checking if user_id in dashboard
        member = DashBoard.query.join(User, DashBoard.users).filter(
            and_(DashBoard.id == dashboard_id,
                 User.chat_id == user_id)).first()
        if task.dashboard_id == dashboard_id and member:
            task.users.append(user)
            db.session.commit()
            return {}, 201
        return "Either access is restricted or wrong dashboard", 409

    def patch(self, user_id, dashboard_id, task_id):
        """Updates task details. Checks if the user is in the dashboard"""

        data = request.get_json()
        # checking if user_id in dashboard
        member = DashBoard.query.join(User, DashBoard.users).filter(
            and_(DashBoard.id == dashboard_id,
                 User.chat_id == user_id)).first()

        if member:
            try:
                task = db.session.query(Task).filter_by(id=task_id)

                if data.get('admin') is not None and \
                        task.first().admin_id != data.get('admin') \
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

    def delete(self, user_id, dashboard_id, task_id):
        task = Task.query.get(task_id)

        member = DashBoard.query.join(User, DashBoard.users).filter(
            and_(DashBoard.id == dashboard_id,
                 User.chat_id == user_id)).first()

        if task.dashboard_id == dashboard_id and member:
            try:
                t = db.session.query(Task).filter_by(id=task_id)
                t.delete()
                db.session.commit()
                return {}, 200
            except AttributeError:
                return 'Not found', 404
        return "Either access is restricted or wrong dashboard", 409


class UserTaskComments(Resource):

    def get(self, user_id, dashboard_id, task_id):
        task = Task.query.get(task_id)

        member = DashBoard.query.join(User, DashBoard.users).filter(
           and_(DashBoard.id == dashboard_id, User.chat_id == user_id)).first()
        try:
            if member and task.dashboard_id == dashboard_id:
                return serialize_multiple(task.comments), 200
        except AttributeError:
            return "Not found", 404

        return "Either access is restricted or wrong dashboard", 409

    def post(self, user_id, dashboard_id, task_id):
        """Only task members, task admin and dashboard admin can
        leave comments"""

        data = request.get_json()
        task = Task.query.get(task_id)
        d = DashBoard.query.get(dashboard_id)
        member = Task.query.join(User, Task.users).filter(
            and_(Task.id == task_id, User.chat_id == user_id)).first()

        try:
            if task.dashboard_id == dashboard_id:
                if member or task.admin == user_id or d.id == user_id:
                    c = Comment(sender=user_id, task_id=task_id, **data)
                    db.session.add(c)
                    db.session.flush()
                    id_ = c.id
                    db.session.commit()
                    # sending a new comment notification
                    init_event_creation('comments', c.serialize())
                    return {'id': id_}, 201
            return "Either access is restricted or wrong dashboard", 409
        except AttributeError:
            return 'Not found', 404
