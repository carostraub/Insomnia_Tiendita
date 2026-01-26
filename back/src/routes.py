import os
from dotenv import load_dotenv
import cloudinary.uploader
from flask_cors import cross_origin, CORS
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from models  import db, product_category, Product, Category,Client, Address, Order, OrderDetail, Review, Coupon
#falta hacer decorador y config imagenes

api = Blueprint("api", __name__)
load_dotenv()

@api.route('/register', methods=['POST'])
def register():
    email = request.form.get("email")
    password = request.form.get("password")
    name = request.form.get("name")
    subscribe = request.form.get("subscribe", "false").lower() == "true"

    if not all([email, password, name]):
        return jsonify({"error":"Hay que completar todos los campos obligatorios"}), 400
    if Client.query.filter_by(email=email).first():
        return jsonify({"error":"Este mail ya esta registrado"}), 409
    

    client = Client(
        email = email,
        name = name,
        subscribe = subscribe,
        admin = False
    )
    client.set_password(password)

    try: 
        db.session.add(client)
        db.session.commit()
        access_token = create_access_token(identity=client.id)

        return jsonify({
            "message": "Bienvenido al club de Insomnia Tiendita",
            "client": client.serialize(),
            "access_token": access_token
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":"Error en el servidor"}), 500
    
@api.route('/setup', methods=['POST'])
def set_up():
    
    email = request.form.get("email")
    password = request.form.get("password")
    name = request.form.get("name")
    setup_token = request.form.get("setup_token")
    

    expected = os.getenv("SETUP_TOKEN")
    
    if Client.query.filter_by(admin=True).first():
        return jsonify({"error":"El setup ya fue completado"}), 403
    if not all([email, password, name, setup_token]):
        return jsonify({"error":"Hay que completar todos los campos obligatorios"}), 400
    if expected is None:
        return jsonify({"error":"Setup Token no configurado en servidor"}), 500
    if setup_token != expected:
        return jsonify({"error":"El SETUP_TOKEN no coincide"}), 403
    if Client.query.filter_by(email=email).first():
        return jsonify({"error":"Este mail ya esta registrado"}), 409
        
    email = email.strip().lower()
    

    client = Client(
        email = email,
        name = name,
        admin = True,
        subscribe = False

    )
    client.set_password(password)
    try:
        db.session.add(client)
        db.session.commit()
        access_token = create_access_token (identity=client.id)
        return jsonify ({
            "message": "El administrador ha sido cnofigurado exitosamente",
            "client": client.serialize(),
            "access_token": access_token
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":"Error en el servidor"}), 500


