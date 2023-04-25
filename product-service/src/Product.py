from db import db  # SQLAlchemy()
import logging

log = logging.getLogger(__name__)

class Product(db.Model):
    __tablename__ = 'products' # SQLAlchemy() attribute

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __init__(self, id, name):  # create objects in the database
        self.id = id
        self.name = name

    @classmethod
    def find_by_id(cls, _id):
        log.debug(f'Find product by id: {_id}')
        return cls.query.get(_id)

    @classmethod
    def find_all(cls):
        log.debug('Query for all products')
        return cls.query.all()

    def save_to_db(self):
        log.debug(f'Save Product to database: id= {self.id}, name={self.name}')
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        log.debug(f'Delete Product from database: id= {self.id}, name={self.name}')
        db.session.delete(self)  # session works similar to cursor
        db.session.commit()

    @property
    def json(self):  # used decorator to set property (not method)
        return {
            "id": self.id,
            "name": self.name
        }