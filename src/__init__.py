from flask import Flask, Response, request, jsonify
from datetime import datetime
import json
from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS

# Create the Flask application object.
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/courses'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

CORS(app)
