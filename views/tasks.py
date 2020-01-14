from flask_restful import Resource

from models import Task, serialize_multiple
from utils.validator import ModelValidator


class TaskUsers(Resource):

    def get(self, task_id):
        task = Task.query.get(task_id)
        return serialize_multiple(task.users)


class TaskComments(Resource):

    def get(self, task_id):
        task = Task.query.get(task_id)
        return serialize_multiple(task.comments)