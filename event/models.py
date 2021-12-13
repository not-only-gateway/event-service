from sqlalchemy.exc import SQLAlchemyError
from app import db


class Event(db.Model):
    __tablename__ = 'evento'

    id = db.Column('codigo_id',db.BigInteger, primary_key=True)
    start_date = db.Column('data_inicio', db.BigInteger, nullable=False)
    elapsed_time = db.Column('tempo_gasto', db.BigInteger, nullable=False)
    package_received = db.Column('pacote_recebido', db.BigInteger)
    package_sent = db.Column('pacote_entregue', db.BigInteger)
    service = db.Column('servico', db.BigInteger, db.ForeignKey('servico.codigo_id', on_delete='PROTECT'),
                        nullable=False)
    instance = db.Column('instancia', db.BigInteger, db.ForeignKey('instancia.codigo_id', on_delete='PROTECT'),
                        nullable=False)
    endpoint = db.Column('endpoint', db.String, db.ForeignKey('endpoint.uri', on_delete='PROTECT'),
                         nullable=False)

    def __init__(self, data):
        for key in data.keys():
            if hasattr(self, key):
                setattr(self, key, data.get(key, None))
        db.session.add(self)
        db.session.commit()
