from flask_restful import Resource

from models import Task, serialize_multiple


class TaskUsers(Resource):

    def get(self, task_id):
        try:
            task = Task.query.get(task_id)
            return serialize_multiple(task.users), 200
        except AttributeError:
            return "Not found", 404


class TaskComments(Resource):

    def get(self, task_id):
        try:
            task = Task.query.get(task_id)
            return serialize_multiple(task.comments), 200
        except AttributeError:
            return "Not found", 404
