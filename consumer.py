import sys
import pika, json
from pika import exceptions
from sqlalchemy.exc import SQLAlchemyError, PendingRollbackError
from datetime import datetime
from app import db
from flask_utils.messaging import consumer
from service.models import Instance, Endpoint, Service
from event.models import Event

def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        if properties.content_type == 'service':
            try:
                service = Service.query.get(data.get('id', None))
                if service is None:
                    Service(data)
            except (SQLAlchemyError, PendingRollbackError):
                pass
        elif properties.content_type == 'instance':
            try:
                instance = Instance.query.get(data.get('id', None))
                if instance is None:
                    Instance(data)
            except (SQLAlchemyError, PendingRollbackError):
                pass
        elif properties.content_type == 'endpoint':
            try:
                endpoint = Endpoint.query.get(data.get('uri', None))
                if endpoint is None:
                    Endpoint(data)
            except (SQLAlchemyError, PendingRollbackError):
                pass
        elif properties.content_type == 'event':
            try:
                Event(data)
            except (SQLAlchemyError, PendingRollbackError):
                pass
    except json.JSONDecodeError:
        pass


consumer(callback=callback, queue='structural')
