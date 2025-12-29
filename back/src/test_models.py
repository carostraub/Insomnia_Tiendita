import unittest
from datetime import datetime, timezone, timedelta
from models import db, Product, Order, OrderDetail, Client
from app import create_app  # Necesitarás crear la app para el contexto



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
    
    def test_products_no_discount(self):
        """Test: 3 Produtos sin descuento con cliente"""
        client = Client(
            name = "Client Test",
            email = "test@test.cl"
            )
        client.set_password("password123")
        db.session.add(client)
        

        product1 = Product(
            name="Producto Sin Descuento",
            price=10000,
            discount=0,
            discount_expiration=None
        )
        db.session.add(product1)
        db.session.commit()
        order = Order(
            client_id = client.id,
            shipping_address = "Street 123",
            total = 0
        )
        db.session.add(order)
        db.session.commit()

        detail1 = OrderDetail(
            order_id = order.id,
            product_id = product1.id,
            quantity = 3,
            unit_price =product1.current_price 
        )
        db.session.add(detail1)
        db.session.commit()

        total = order.calculate_total()
        expected_total = 30000
        self.assertEqual(total, expected_total)

    def test_order_with_discounts(self):
        """Test: Productos con distintos descuentos y sin client_id""" 
        future_date = datetime.now(timezone.utc) + timedelta(days=1)
        product1 =  Product(
            name="Producto Con Descuento",
            price=10000,
            discount=20,  # 20% de descuento
            discount_expiration=future_date
        )

        past_date = datetime.now(timezone.utc) - timedelta(days=1)
        product2 = Product(
            name="Producto Descuento Expirado",
            price=10000,
            discount=30,  # 30% de descuento
            discount_expiration = past_date
        )
        product3 = Product(
            name="Producto Descuento Permanente",
            price=5000,
            discount=15,
            discount_expiration = None  # Descuento permanente
        )
    

        db.session.add_all([product1, product2, product3])
        db.session.commit()
        order = Order(
            client_id = None,
            shipping_address = "Street 123",
            total = 0
        )

        db.session.add(order)
        db.session.commit()

        detail1 = OrderDetail(
            order_id = order.id,
            product_id = product1.id,
            quantity = 2,
            unit_price = product1.current_price
        )

        detail2 = OrderDetail(
            order_id = order.id,
            product_id = product2.id,
            quantity = 3,
            unit_price = product2.current_price
        )

        detail3 = OrderDetail(
            order_id = order.id,
            product_id = product3,
            quantity = 1,
            unit_price = product3.current_price
        )
        db.session.add_all([detail1, detail2, detail3])
        db.session.commit()

        total = order.calculate_total()
        expected_total = 50250 
        self.assertEqual(total, expected_total)

        


        

if __name__ == '__main__':
    unittest.main()

""" import unittest
from datetime import datetime, timezone, timedelta
from models import db, Product, Order, OrderDetail, Client
from app import create_app

class TestOrderModels(unittest.TestCase):
    def setUp(self):
        #Configuración antes de cada test
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        #Limpieza después de cada test
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_calculate_total_no_discount(self):
        #Test: Calcular total con 3 productos sin descuento
        # 1. Crear cliente
        cliente = Client(
            name="Cliente Test",
            email="test@test.com"
        )
        cliente.set_password("password123")
        db.session.add(cliente)
        
        # 2. Crear productos sin descuento
        producto1 = Product(
            name="Producto 1",
            price=10000,
            discount=0,
            discount_expiration=None,
            stock=10
        )
        
        producto2 = Product(
            name="Producto 2",
            price=15000,
            discount=0,
            discount_expiration=None,
            stock=5
        )
        
        producto3 = Product(
            name="Producto 3",
            price=5000,
            discount=0,
            discount_expiration=None,
            stock=20
        )
        
        db.session.add_all([producto1, producto2, producto3])
        db.session.commit()
        
        # 3. Crear orden
        orden = Order(
            client_id=cliente.id,
            shipping_address="Calle Test 123",
            total=0  # Temporal, se calculará
        )
        db.session.add(orden)
        db.session.commit()
        
        # 4. Agregar productos a la orden
        detalle1 = OrderDetail(
            order_id=orden.id,
            product_id=producto1.id,
            quantity=2,  # 2 unidades
            unit_price=producto1.current_price  # 10000
        )
        
        detalle2 = OrderDetail(
            order_id=orden.id,
            product_id=producto2.id,
            quantity=1,  # 1 unidad
            unit_price=producto2.current_price  # 15000
        )
        
        detalle3 = OrderDetail(
            order_id=orden.id,
            product_id=producto3.id,
            quantity=3,  # 3 unidades
            unit_price=producto3.current_price  # 5000
        )
        
        db.session.add_all([detalle1, detalle2, detalle3])
        db.session.commit()
        
        # 5. Calcular total
        total_calculado = orden.calculate_total()  # ← CON paréntesis
        
        # 6. Verificar cálculo manual
        # Producto1: 2 × 10000 = 20000
        # Producto2: 1 × 15000 = 15000  
        # Producto3: 3 × 5000 = 15000
        # TOTAL: 20000 + 15000 + 15000 = 50000
        total_esperado = 50000
        
        self.assertEqual(total_calculado, total_esperado)
        print(f"✅ Total calculado: ${total_calculado:,}")
    
    def test_calculate_total_with_product_discount(self):
       #Test: Calcular total con productos con descuento
        # Crear productos con descuento
        futuro = datetime.now(timezone.utc) + timedelta(days=1)
        
        producto_descuento = Product(
            name="Producto con 50% descuento",
            price=20000,
            discount=50,  # 50% de descuento
            discount_expiration=futuro,
            stock=10
        )
        
        producto_normal = Product(
            name="Producto normal",
            price=10000,
            discount=0,
            discount_expiration=None,
            stock=10
        )
        
        db.session.add_all([producto_descuento, producto_normal])
        
        # Crear orden y detalles
        orden = Order(
            shipping_address="Calle Test 456",
            total=0
        )
        db.session.add(orden)
        db.session.commit()
        
        # Agregar productos
        # Producto con descuento: 20000 - 50% = 10000
        detalle1 = OrderDetail(
            order_id=orden.id,
            product_id=producto_descuento.id,
            quantity=2,  # 2 unidades
            unit_price=producto_descuento.current_price  # 10000 (con descuento)
        )
        
        # Producto normal: 10000
        detalle2 = OrderDetail(
            order_id=orden.id,
            product_id=producto_normal.id,
            quantity=1,  # 1 unidad
            unit_price=producto_normal.current_price  # 10000
        )
        
        db.session.add_all([detalle1, detalle2])
        db.session.commit()
        
        # Calcular total
        total = orden.calculate_total()
        
        # Verificar: (2 × 10000) + (1 × 10000) = 30000
        self.assertEqual(total, 30000)
        print(f"✅ Total con descuentos: ${total:,}")

if __name__ == '__main__':
    unittest.main(verbosity=2) """