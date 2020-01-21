from settings import db

# TODO DELETE tasks, comments and users upon deleting a dashboard!
# TODO create validator
# TODO solve issues adding a few same rows

dashboard_users = db.Table(
    "dashboard_users", db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("dashboard_id", db.Integer, db.ForeignKey("dashboards.id"))
)

task_users = db.Table(
    "task_users", db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("task_id", db.Integer, db.ForeignKey("tasks.id"))
)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(70), unique=True, nullable=False)
    email = db.Column(db.String(70), unique=True, nullable=False)

    comments = db.relationship("Comment", backref='author')
    dashboards = db.relationship('DashBoard', secondary=dashboard_users,
                                 backref=db.backref('users', lazy=True))
    tasks = db.relationship('Task', secondary=task_users,
                            backref=db.backref('users', lazy=True))

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }


class DashBoard(db.Model):
    __tablename__ = 'dashboards'

    id = db.Column(db.Integer, primary_key=True)
    dashboard_name = db.Column(db.String(100), unique=True, nullable=False)
    admin = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    tasks = db.relationship('Task', backref='dashboard')

    def __repr__(self):
        return '<Dashboard %r>' % self.dashboard_name

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "dashboard_name": self.dashboard_name,
            "admin": self.admin
        }


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=True)
    admin_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    dashboard_id = db.Column(db.Integer, db.ForeignKey("dashboards.id"),
                             nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    status = db.Column(db.String(50), default="TO DO")

    comments = db.relationship('Comment', backref='task')

    def __repr__(self):
        return '<Task %r>' % self.task_name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.task_name,
            "text": self.text,
            "admin": self.admin_id,
            "dashboard": self.dashboard_id,
            "created at": str(self.created_at),
            "status": self.status
        }


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text(1000), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"),
                          nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"),
                        nullable=False)

    def __repr__(self):
        return '<Comment %r>' % self.id

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "comment": self.text,
            "sender": self.sender_id,
            "task": self.task_id
        }


def serialize_multiple(objects: list) -> list:
    return [obj.serialize() for obj in objects]


if __name__ == '__main__':
    db.create_all()
