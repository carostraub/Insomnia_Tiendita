import os
import cloudinary.uploader
from flask_cors import cross_origin, CORS
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from models  import db, product_category, Product, Category,Client, Address, Order, OrderDetail, Review, Coupon
#falta hacer decorador y config imagenes

api = Blueprint("api", __name__)