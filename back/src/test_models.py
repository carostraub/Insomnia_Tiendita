import unittest
from datetime import datetime, timezone, timedelta
from models import db, Product
from app import create_app  # Necesitarás crear la app para el contexto

def current_price_no_discount(self):
    """Test: Precio sin descuento"""
    # Crear producto sin descuento
    product = Product(
            name="Producto Sin Descuento",
            price=10000,
            discount=0,
            discount_expiration=None
        )
def current_price_with_active_discount(self):
    """Test: Precio con descuento activo"""
    # Crear producto con descuento activo (expira en el futuro)
    future_date = datetime.now(timezone.utc) + timedelta(days=1)
    product = Product(
            name="Producto Con Descuento",
            price=10000,
            discount=20,  # 20% de descuento
            discount_expiration=future_date
        )
        # Precio debería ser: 10000 * (1 - 0.20) = 8000
    expected_price = round(10000 * (1 - 20/100))

def current_price_with_expired_discount(self):
    """Test: Precio con descuento expirado"""
    # Crear producto con descuento expirado
    past_date = datetime.now(timezone.utc) - timedelta(days=1)
    product = Product(
            name="Producto Descuento Expirado",
            price=10000,
            discount=30,  # 30% de descuento
            discount_expiration=past_date
        )

def current_price_rounding(self):
    """Test: Verificar que el precio se redondea correctamente"""
    product = Product(
            name="Producto Con Decimales",
            price=9999,
            discount=60,  # 60% de descuento
            discount_expiration=datetime.now(timezone.utc) + timedelta(days=1)
        )
    
def active_discount_no_expiration(self):
    """Test: Descuento sin fecha de expiración"""
    product = Product(
            name="Producto Descuento Permanente",
            price=5000,
            discount=15,
            discount_expiration = None  # Descuento permanente
        )

def active_discount_zero_discount(self):
    """Test: Descuento en 0% no debe estar activo"""
    product = Product(
            name="Producto Cero Descuento",
            price=8000,
            discount=0,  # 0% de descuento
            discount_expiration=datetime.now(timezone.utc) + timedelta(days=1)
        ) 
    
def active_discount_negative_discount(self):
        """Test: Descuento en -10% no debe estar activo"""
        product = Product(
            name="Producto Descuento Negativo",
            price=8000,
            discount=-10,  # 0% de descuento
            discount_expiration=datetime.now(timezone.utc) + timedelta(days=1)
        )

class TestProductModels(unittest.TestCase):
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.app = create_app('testing')  # Configuración para testing
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        """Limpieza después de cada test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_current_price_no_discount(self):
        """Test: Precio sin descuento"""
        # Crear producto sin descuento
        product = Product(
            name="Producto Sin Descuento",
            price=10000,
            discount=0,
            discount_expiration=None
        )
        
        # Verificar que el precio actual es el precio original
        self.assertEqual(product.current_price, 10000)
        self.assertFalse(product.active_discount)
    
    def test_current_price_with_active_discount(self):
        """Test: Precio con descuento activo"""
        # Crear producto con descuento activo (expira en el futuro)
        future_date = datetime.now(timezone.utc) + timedelta(days=1)
        product = Product(
            name="Producto Con Descuento",
            price=10000,
            discount=20,  # 20% de descuento
            discount_expiration=future_date
        )
        
        # Precio debería ser: 10000 * (1 - 0.20) = 8000
        expected_price = round(10000 * (1 - 20/100))
        self.assertEqual(product.current_price, expected_price)
        self.assertTrue(product.active_discount)
    
    def test_current_price_with_expired_discount(self):
        """Test: Precio con descuento expirado"""
        # Crear producto con descuento expirado
        past_date = datetime.now(timezone.utc) - timedelta(days=1)
        product = Product(
            name="Producto Descuento Expirado",
            price=10000,
            discount=30,  # 30% de descuento
            discount_expiration=past_date
        )
        
        # Debería usar el precio original porque el descuento expiró
        self.assertEqual(product.current_price, 10000)
        self.assertFalse(product.active_discount)
    
    def test_current_price_rounding(self):
        """Test: Verificar que el precio se redondea correctamente"""
        product = Product(
            name="Producto Con Decimales",
            price=9999,
            discount=60,  # 60% de descuento
            discount_expiration=datetime.now(timezone.utc) + timedelta(days=1)
        )
        
        # 9999 * 0.4 = 3999.6 → debería redondear a 4000
        self.assertEqual(product.current_price, 4000)
    
    def test_active_discount_no_expiration(self):
        """Test: Descuento sin fecha de expiración"""
        product = Product(
            name="Producto Descuento Permanente",
            price=5000,
            discount=15,
            discount_expiration=None  # Descuento permanente
        )
        
        self.assertTrue(product.active_discount)
        self.assertEqual(product.current_price, round(5000 * 0.85))  # 15% off
    
    def test_active_discount_zero_discount(self):
        """Test: Descuento en 0% no debe estar activo"""
        product = Product(
            name="Producto Cero Descuento",
            price=8000,
            discount=0,  # 0% de descuento
            discount_expiration=datetime.now(timezone.utc) + timedelta(days=1)
        )
        
        self.assertFalse(product.active_discount)
        self.assertEqual(product.current_price, 8000)

    def test_active_discount_negative_discount(self):
        """Test: Descuento en -10% no debe estar activo"""
        product = Product(
            name="Producto Descuento Negativo",
            price=8000,
            discount=-10,  # 0% de descuento
            discount_expiration=datetime.now(timezone.utc) + timedelta(days=1)
        )
        
        self.assertFalse(product.active_discount)
        self.assertEqual(product.current_price, 8000)


class TestOrderModels(unittest.TestCase):
    def setUp(self):
        """Configuración antes de cada test"""
        self.app = create_app('testing')  # Configuración para testing
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        """Limpieza después de cada test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

if __name__ == '__main__':
    unittest.main()