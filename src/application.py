from flask import Flask, Response, request
from datetime import datetime
import json
from flask_cors import CORS

# Create the Flask application object.
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

CORS(app)


@app.post("/sections/new_section")
def add_new_section():
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)

