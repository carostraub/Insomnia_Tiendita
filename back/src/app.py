import cloudinary
import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db
from routes import api
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

# Configuración de Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

# ========== ¡IMPORTANTE! MANTENER ESTA FUNCIÓN PARA TESTS ==========
def create_app(config_name='testing'):
    """
    Factory para crear la aplicación Flask.
    config_name: 'testing' para tests, cualquier otro para desarrollo
    """
    app = Flask(__name__)
    
    if config_name == 'testing':
        # Configuración para testing (BD en memoria)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
    else:
        # Configuración para desarrollo/producción
        app.config['DEBUG'] = True 
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    
    # Configuración común
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET') 
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=2)
    
    # Inicializar extensiones
    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)
    CORS(app)
    
    return app

# ========== CREAR APP PRINCIPAL PARA DESARROLLO ==========
# Esto es lo que se ejecuta cuando corres el servidor
app = create_app('development')  # 'development' no es 'testing', usa BD normal

# Ruta principal
@app.route('/')
def main():
    return jsonify({"message": "REST API FLASK"}), 200

# Registrar el blueprint de rutas
app.register_blueprint(api, url_prefix="/api")

if __name__ == '__main__':
    app.run()