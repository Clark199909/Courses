import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS

pymysql.install_as_MySQLdb()

# Create the Flask application object.
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

# Need to change username and password before running application.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:dbuserbdbuser@localhost/courses'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

CORS(app)
