from flask import jsonify
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from app import app
from app import db
from sqlalchemy import and_
import pandas
from sklearn.tree import DecisionTreeClassifier
from event.models import Event
from flask_utils.api import ApiView

api = ApiView(
    class_instance=Event,
    identifier_attr='id',
    relationships=[],
    db=db
)


@app.route('/api/predict/<service>/<path:endpoint>/<start_time>/<limit>', methods=['GET'])
def list(service=None, endpoint=None, start_time=None, limit=1000):
    if service is not None and endpoint is not None:
        data = Event.query.filter(Event.start_date <= start_time).limit(limit)
        parsed_data = []
        for i in data:
            parsed_data.append(api.parse_model(i))

        model = DecisionTreeClassifier()

        dataframe = pandas.DataFrame(parsed_data)

        X = dataframe.drop(columns=['instance', 'elapsed_time', 'package_received', 'package_sent'])
        y = dataframe.drop(columns=['service', 'package_received', 'package_sent', 'endpoint', 'start_date'])

        model.fit(X.values, y)

        prediction = model.predict([[service, endpoint]])

        return jsonify({
            'best_service_instance': prediction[1],
            'expected_response_time': prediction[0],
        }), 200

    else:
        return jsonify({'status': 'error', 'description': 'not_found', 'code': 404}), 404
