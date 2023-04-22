from db import db  # SQLAlchemy()


class Product(db.Model):
    __tablename__ = 'products' # SQLAlchemy() attribute

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __init__(self, id, name):  # create objects in the database
        self.id = id
        self.name = name

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)  # session works similar to cursor
        db.session.commit()

    @property
    def json(self):  # used decorator to set property (not method)
        return {
            "id": self.id,
            "name": self.name
        }