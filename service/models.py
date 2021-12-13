from sqlalchemy.exc import SQLAlchemyError
from app import db


class Service(db.Model):
    __tablename__ = 'servico'

    id = db.Column('codigo_id', db.BigInteger, primary_key=True)

    def __init__(self, data):
        for key in data.keys():
            if hasattr(self, key):
                setattr(self, key, data.get(key, None))
        db.session.add(self)
        db.session.commit()
class Instance(db.Model):
    __tablename__ = 'instancia'

    id = db.Column('codigo_id', db.BigInteger, primary_key=True)
    service = db.Column('servico', db.BigInteger, db.ForeignKey('servico.codigo_id', on_delete='PROTECT'),
                        nullable=False)

    def __init__(self, data):
        for key in data.keys():
            if hasattr(self, key):
                setattr(self, key, data.get(key, None))
        db.session.add(self)
        db.session.commit()

class Endpoint(db.Model):
    __tablename__ = 'endpoint'

    uri = db.Column('uri',db.String, primary_key=True)
    service = db.Column('servico', db.BigInteger, db.ForeignKey('servico.codigo_id', on_delete='PROTECT'),
                        nullable=False)

    def __init__(self, data):
        for key in data.keys():
            if hasattr(self, key):
                setattr(self, key, data.get(key, None))
        db.session.add(self)
        db.session.commit()
