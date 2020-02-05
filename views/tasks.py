from flask_restful import Resource

from models import Task, Comment, serialize_multiple
from utils.validator import ModelValidator

# TODO use model validator


class Tasks(Resource):

    def get(self, task_id):
        return ModelValidator.get_by_id(task_id)


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


class TaskCommentsDetailed(Resource):

    def get(self, comment_id):
        return ModelValidator(Comment).get_by_id(comment_id)

