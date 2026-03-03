import os
import traceback
from dotenv import load_dotenv
import cloudinary.uploader
from flask_cors import cross_origin, CORS
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from models import db, product_category, Product, Category, Client, Address, Order, OrderDetail, Review, Coupon
from decorators import admin_required
from config_img import allowed_files

api = Blueprint("api", __name__)
load_dotenv()

@api.route('/register', methods=['POST'])
def register():
    email = request.form.get("email")
    password = request.form.get("password")
    name = request.form.get("name")
    subscribe = request.form.get("subscribe", "false").lower() == "true"

    if not all([email, password, name]):
        return jsonify({"error": "Hay que completar todos los campos obligatorios"}), 400

    email = email.strip().lower()

    if Client.query.filter_by(email=email).first():
        return jsonify({"error": "Este mail ya esta registrado"}), 409

    client = Client(
        email=email,
        name=name,
        subscribe=subscribe,
        admin=False
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

    except Exception:
        db.session.rollback()
        traceback.print_exc()  # 👈 muestra el error real en consola
        return jsonify({"error": "Error en el servidor"}), 500


@api.route('/setup', methods=['POST'])
def set_up():
    print("Entro a setup", flush=True)

    email = request.form.get("email")
    password = request.form.get("password")
    name = request.form.get("name")
    setup_token = request.form.get("setup_token")

    expected = os.getenv("SETUP_TOKEN")

    if Client.query.filter_by(admin=True).first():
        return jsonify({"error": "El setup ya fue completado"}), 403

    if not all([email, password, name, setup_token]):
        return jsonify({"error": "Hay que completar todos los campos obligatorios"}), 400

    if expected is None:
        return jsonify({"error": "Setup Token no configurado en servidor"}), 500

    if setup_token != expected:
        return jsonify({"error": "El SETUP_TOKEN no coincide"}), 403

    email = email.strip().lower()

    if Client.query.filter_by(email=email).first():
        return jsonify({"error": "Este mail ya esta registrado"}), 409

    client = Client(
        email=email,
        name=name,
        admin=True,
        subscribe=False
    )
    client.set_password(password)

    try:
        db.session.add(client)
        db.session.commit()
        access_token = create_access_token(identity=client.id)

        return jsonify({
            "message": "El administrador ha sido configurado exitosamente",
            "client": client.serialize(),
            "access_token": access_token
        }), 201

    except Exception:
        db.session.rollback()
        traceback.print_exc()  # 👈 muestra el error real en consola
        return jsonify({"error": "Error en el servidor"}), 500


@api.route('/login', methods=['POST'])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    if not email:
        return jsonify({"error": "El email es requerido"}), 400
    if not password:
        return jsonify({"error": "La contraseña es requerida"}), 400

    email = email.strip().lower()

    client = Client.query.filter_by(email=email).first()
    if not client or not client.check_password(password):
        return jsonify({"error": "Datos incorrectos"}), 401

    access_token = create_access_token(identity=client.id)

    return jsonify({
        "access_token": access_token,
        "client": client.serialize()
    }), 200

@api.route('/profile', methods=["GET"])
@jwt_required
def profile():
    user_id = get_jwt_identity()
    user = db.session.get(Client, user_id)

    if not user:
        return jsonify({"error":"Usuario no encontrado"}), 400
    return jsonify(user.serialize()), 200

@api.route('/products', methods=["POST"])
@admin_required()
def new_porduct():
    if 'name' not in request.form or not request.form['name']:
        return jsonify({"error":"El nombre es obligatorio"}), 400
    if  'description' not in request.form or not request.form['description'] :
        return jsonify({"error":"La descripción es obligatoria"}), 400
    if 'price' not in request.form or not request.form['price']:
        return jsonify({"error":"El precio es obligatorio"}), 400
    
    image_url=None
    if 'photo' in request.files:
        image=request.files['photo']
     
    if image.filename == "":
        return jsonify({"error":"Nombre del archivo vacío"}), 400
    if not allowed_files(image.filename):
        return jsonify({"error":"Formato de archivo no permitido"}), 400
    
    try: #para subir la imagen a cloudinary
        upload_result = cloudinary.uploader.upload(image, folder="products")
        image_url=upload_result['secure_url']

    except Exception as e:
            return jsonify({"error": f"Error al subir imagen: {str(e)}"}), 500
    try:
        new_product = Product(
            name=request.form['name'],
            description=request.form['description'],
            price=float(request.form['price']),
            img=image_url
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({
            "msg":"Producto creado",
            "product":new_product.serialize()
            }), 201
    except ValueError:
        db.session.rollback()
        return jsonify({"error":"Precio o stock inválido"}), 400
    except Exception as e:  # Otros errores de BD
        db.session.rollback()
        return jsonify({"error": f"Error en la base de datos: {str(e)}"}), 500
