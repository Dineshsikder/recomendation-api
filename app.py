
# app.py
import os
import logging
from flask import Flask
from controller.controller import recommendation_controller
from flask_restx import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)
# app.config['JWT_SECRET_KEY'] = os.urandom(32)
# app.config['JWT_TOKEN_LOCATION'] = ['headers'] 
# app.config['JWT_HEADER_NAME'] = 'Authorization'
# app.config['JWT_HEADER_TYPE'] = 'Bearer'  # Specify the JWT header type
# jwt = JWTManager(app)

CORS(app)  # Allow CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api = Api(app)
api.add_namespace(recommendation_controller)

if __name__ == '__main__':
    app.run(debug=True)

