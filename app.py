from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import env

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = env.DATABASE + '://'+ env.USER+':'+env.PASSWORD+'@'+env.HOST_NAME+'/'+env.DATABASE_NAME
db = SQLAlchemy(app)
CORS(app)

from service.models import Service, Instance, Endpoint
from event.models import Event

from event import views

db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1025)
