from settings import app, api
from views.users import Users, SingleUser, UserStats
from views.dashboards import Dashboards, SingleDashboard, DashboardUsers, \
    DashboardTasks, DashboardTaskUsers
from views.user_dashboards import UserDashboards, UserDashboardsDetailed, \
    UserTasks
from views.user_tasks import UserTasksDetailed, UserTaskComments

api.add_resource(Users, '/users')
api.add_resource(SingleUser, '/users/<int:user_id>')
api.add_resource(UserStats, '/users/<int:user_id>/data')


api.add_resource(Dashboards, '/dashboards')
api.add_resource(SingleDashboard, '/dashboards/<int:dashboard_id>')
api.add_resource(DashboardUsers, '/dashboards/<int:dashboard_id>/users')
api.add_resource(DashboardTasks, '/dashboards/<int:dashboard_id>/tasks')
api.add_resource(DashboardTaskUsers,
                 '/dashboards/<int:dashboard_id>/tasks/<int:task_id>/users')

# ???????
api.add_resource(UserDashboards, '/users/<int:user_id>/dashboards')
# ?????- the same as query from /stats
api.add_resource(UserDashboardsDetailed,
                 '/users/<int:user_id>/dashboards/<int:dashboard_id>')
api.add_resource(UserTasks,
                 '/users/<int:user_id>/dashboards/<int:dashboard_id>/tasks')
api.add_resource(
    UserTasksDetailed,
    '/users/<int:user_id>/dashboards/<int:dashboard_id>/tasks/<int:task_id>')

api.add_resource(
    UserTaskComments,
    '/users/<int:user_id>/dashboards/<int:dashboard_id>/tasks/<int:task_id>/comments'
)


if __name__ == '__main__':
    app.run(debug=True)
