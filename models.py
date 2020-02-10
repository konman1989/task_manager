from settings import db

dashboard_users = db.Table(
    "dashboard_users", db.Model.metadata,
    db.Column("user_id", db.Integer,
              db.ForeignKey("users.chat_id", ondelete="CASCADE")),
    db.Column("dashboard_id", db.Integer,
              db.ForeignKey("dashboards.id", ondelete="CASCADE"))
)

task_users = db.Table(
    "task_users", db.Model.metadata,
    db.Column("user_id", db.Integer,
              db.ForeignKey("users.chat_id", ondelete="CASCADE")),
    db.Column("task_id", db.Integer,
              db.ForeignKey("tasks.id", ondelete="CASCADE"))
)

user_subscriptions = db.Table(
    "user_subscriptions", db.Model.metadata,
    db.Column("user_id", db.Integer,
              db.ForeignKey("users.chat_id", ondelete="CASCADE"),
              primary_key=True),
    db.Column("event", db.String,
              db.ForeignKey("events.event", ondelete="CASCADE"),
              primary_key=True)
)


class User(db.Model):
    __tablename__ = 'users'

    chat_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(32), unique=True, nullable=False)

    dashboards = db.relationship('DashBoard', secondary=dashboard_users,
                                 backref=db.backref('users', lazy=True))
    tasks = db.relationship('Task', secondary=task_users,
                            backref=db.backref('users', lazy=True))
    comments = db.relationship("Comment", backref='author')
    subscriptions = db.relationship('Event', secondary=user_subscriptions,
                                    backref=db.backref("subscribers",
                                                       lazy=True))

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self) -> dict:
        return {
            "chat_id": self.chat_id,
            "username": self.username,
            "email": self.email
        }


class DashBoard(db.Model):
    __tablename__ = 'dashboards'

    id = db.Column(db.Integer, primary_key=True)
    dashboard_name = db.Column(db.String(32), nullable=False)
    admin = db.Column(db.Integer,
                      db.ForeignKey("users.chat_id", ondelete='CASCADE'),
                      nullable=False)

    tasks = db.relationship('Task', backref='dashboard')
    admin_name = db.relationship('User', backref='dashboard')

    def __repr__(self):
        return '<Dashboard %r>' % self.dashboard_name

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.dashboard_name,
            "admin": self.admin_name.username,
            "admin_id": self.admin
        }


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(32), nullable=False)
    text = db.Column(db.Text, nullable=True)
    admin = db.Column(db.Integer,
                      db.ForeignKey("users.chat_id", ondelete='CASCADE'),
                      nullable=False)
    dashboard_id = db.Column(db.Integer, db.ForeignKey("dashboards.id",
                                                       ondelete='CASCADE'),
                             nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    status = db.Column(db.String(32), default="TO DO")

    comments = db.relationship('Comment', backref='task')
    admin_name = db.relationship('User', backref='task')

    def __repr__(self):
        return '<Task %r>' % self.task_name

    def serialize(self):
        return {
            "id": self.id,
            "task_name": self.task_name,
            "text": self.text,
            "admin": self.admin,
            "admin_name": self.admin_name.username,
            "dashboard_id": self.dashboard_id,
            "dashboard": self.dashboard.dashboard_name,
            "created_at": self.created_at.strftime("%d-%m-%Y %H:%M:%S"),
            "status": self.status
        }


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), nullable=False)
    text = db.Column(db.Text, nullable=False)
    sender = db.Column(db.Integer,
                       db.ForeignKey("users.chat_id", ondelete='CASCADE'),
                       nullable=False)
    task_id = db.Column(db.Integer,
                        db.ForeignKey("tasks.id", ondelete='CASCADE'),
                        nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return '<Comment %r>' % self.title

    def serialize(self) -> dict:
        return {
            "id": self.id,
            'title': self.title,
            "comment": self.text,
            "sender": self.author.username,
            "task": self.task.task_name,
            "created_at": self.created_at.strftime("%d-%m-%Y %H:%M:%S")
        }


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(20), nullable=False, unique=True)

    def __repr__(self):
        return '<Event %r>' % self.event

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "event": self.event
        }


def serialize_multiple(objects: list) -> list:
    return [obj.serialize() for obj in objects]


if __name__ == '__main__':
    db.create_all()
