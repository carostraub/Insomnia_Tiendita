from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy

#Tabla de asociación para categorias
product_category =db.Table('product_category',
        db.Column('product_id', db.Integer, db.ForeignKey('products.id')),
        db.Column('category_id', db.Integer, db.ForeignKey('categories.id'))
        )

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String)  
    price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, default=0.0)
    discount_expiration = db.Column(db.DateTime)
    stock = db.Column(db.Integer, default=0)
    img = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    # Relaciones
    order_details = db.relationship('OrderDetail', backref='product', lazy=True)  
    reviews = db.relationship('Review', backref='product', lazy=True)
    categories = db.relationship('Category', secondary=product_category, backref='products')

    @property
    def current_price(self): #Calcular el precio final considerando descuentos
        if self.active_discount:
            return round(self.price *(1 - self.discount/100))
        return self.price #esto sirve en vez de un else por el return anterior
    
    @property
    def active_discount(self): #Verificar que el descuento este activo
        return (self.discount > 0 and (not self.discount_expiration or self.discount_expiration > datetime.now(timezone.utc)))
    
    def serialize(self):
        def formatted_price(value):
            value_rounded = int(round(value))
            return "{:,}".format(value_rounded).replace (",", ".") #Separador por cada 1.000
        
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "original_price": formatted_price(self.price),
            "current_price": formatted_price(self.current_price),
            "discount_percent":round(self.discount, 2) if self.active_discount else None,
            "discount_ends": self.discount_expiration.isoformat() if self.discount_expiration else None,
            "on_sale": self.active_discount,  
            "stock": self.stock,
            "image_url": self.img,  
            "categories": [category.serialize() for category in self.categories], #Relación
            "created_at": self.created_at.isoformat() if self.created_at else None

        }

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    subscribe = db.Column(db.Boolean, default=True)
    admin = db.Column(db.Boolean, default=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    # Relaciones
    orders = db.relationship('Order', backref='client', lazy=True)  
    addresses = db.relationship('Address', backref='client', lazy=True)  
    reviews = db.relationship('Review', backref='client', lazy=True)
    coupons = db.relationship('Coupon', backref='client', lazy=True)  

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def serialize(self):
        return{
           "id":self.id,
            "name":self.name,
            "email":self.email,
            "subscribe":self.subscribe,
            "phone":self.phone,
            "created_at": self.created_at.isoformat() if self.created_at else None 
        }

class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)  
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    comuna = db.Column(db.String(50))