import cloudinary
import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db
#from routes import api
from config import TestingConfig, DevelopmentConfig
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
) 

app = Flask(__name__)
app.config['DEBUG'] = True 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') 
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET') 
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=2)

db.init_app(app)
Migrate(app, db)
jwt = JWTManager(app)
CORS(app) 

def create_app(config_name='default'):
    app = Flask(__name__)
    
    if config_name == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)
    
    db.init_app(app)
    return app
@app.route('/')
def main():
    return jsonify({"message": "REST API FLASK"}), 200

#app.register_blueprint(api, url_prefix="/api")


if __name__ == '__main__':
    app.run()