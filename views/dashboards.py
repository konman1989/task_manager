from flask import request
from flask_restful import Resource

from models import DashBoard, serialize_multiple, Task
from utils.validator import ModelValidator


class Dashboards(Resource):

    def get(self):
        args = request.args.get('query')

        if args is not None:
            return DashBoard.query.filter_by(
                dashboard_name=args).first().serialize(), 200

        return ModelValidator(DashBoard).get()


class SingleDashboard(Resource):

    def get(self, dashboard_id):
        return ModelValidator(DashBoard).get_by_id(dashboard_id)


class DashboardUsers(Resource):

    def get(self, dashboard_id):
        try:
            d = DashBoard.query.get(dashboard_id)
            return [u.serialize() for u in d.users], 200
        except AttributeError:
            return "Not found", 404


class DashboardTasks(Resource):

    def get(self, dashboard_id):
        args = request.args.get('status')
        d = DashBoard.query.get(dashboard_id)

        if args is not None:
            try:
                if args == 'todo':
                    return [t.serialize() for t in d.tasks if
                            t.status == "TO DO"], 200
                elif args == 'inprocess':
                    return [t.serialize() for t in d.tasks if
                            t.status == "IN PROCESS"], 200
                elif args == 'done':
                    return [t.serialize() for t in d.tasks if
                            t.status == "DONE"], 200
            except AttributeError:
                return "Not found", 404
        try:
            return serialize_multiple(d.tasks), 200
        except AttributeError:
            return "Not found", 404


class DashboardStats(Resource):

    def get(self, dashboard_id):
        d = DashBoard.query.get(dashboard_id)
        tasks = serialize_multiple(d.tasks)
        status = [t.get('status') for t in tasks]

        return {'status': status}




