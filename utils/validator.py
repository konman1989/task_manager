from sqlalchemy.exc import IntegrityError, InvalidRequestError

from models import serialize_multiple
from settings import db


class ModelValidator:

    def __init__(self, model):
        self.model = model

    def get(self):
        return serialize_multiple(self.model.query.all()), 200

    def get_by_id(self, model_id):
        try:
            return self.model.query.get(model_id).serialize()
        except AttributeError:
            return "Not found", 404

    def post(self, data):
        try:
            model = self.model(**data)
            db.session.add(model)
            db.session.flush()
            id_ = model.chat_id
            db.session.commit()
            return {"id": id_}, 201
        except TypeError:
            return "Wrong input", 400
        except IntegrityError:
            return "Either data already exists or wrong input", 409

    def patch_by_id(self, model_id, data):
        try:
            db.session.query(self.model).filter_by(chat_id=model_id).update(data)
            db.session.commit()
            return {}, 204

        except InvalidRequestError:
            return "Wrong input", 400

        except IntegrityError:
            return "Either data already exists or wrong input", 409



