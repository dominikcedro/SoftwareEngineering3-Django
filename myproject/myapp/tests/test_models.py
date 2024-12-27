from django.test import TestCase
from ..models import Product, Customer, Order, OrderStatus
from django.core.exceptions import ValidationError


class ProductModelTest(TestCase):
    def test_create_product_with_valid_data(self):
        temp_product = Product.objects.create(name='Temporary product', price=1.99, available=True)
        self.assertEqual(temp_product.name, 'Temporary product')
        self.assertEqual(temp_product.price, 1.99)
        self.assertTrue(temp_product.available)

    def test_create_product_with_negative_price(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='Invalid product', price = -1.99, available = True)
            temp_product.full_clean()

    # product creation with valid data
    def test_create_product_with_valid_data_2(self):
        temp_product = Product.objects.create(name='Temporary product ?', price=3.12, available=True)
        self.assertEqual(temp_product.name, 'Temporary product ?')
        self.assertEqual(temp_product.price, 3.12)
        self.assertTrue(temp_product.available)

    # product creation with ay of the required fields missing
    def test_create_product_with_missing_field(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='Invalid product', price=1.99)
            temp_product.full_clean()

    # product creation with edge values for name lenght
    def test_create_product_with_border_name(self):
        NAME_BORDER_LONG = 'd' * 255
        temp_product = Product(name=NAME_BORDER_LONG, price=3.12, available=True)
        with self.assertRaises(ValidationError):
            temp_product.full_clean()

    # product creation iwht edge valeus for price value
    def test_create_product_with_border_price_low(self):
        PRICE_BORDER_LOW = -1
        temp_product = Product(name='Temporary', price=PRICE_BORDER_LOW, available=True)
        with self.assertRaises(ValidationError):
            temp_product.full_clean()

    def test_create_product_with_border_price_high(self):
        PRICE_BORDER_HIGH = 1000001
        temp_product = Product(name='Temporary', price=PRICE_BORDER_HIGH, available=True)
        with self.assertRaises(ValidationError):
            temp_product.full_clean()

    # product creation with invalid price format
    def test_create_product_with_too_many_decimal_places(self):
        PRICE_TOO_MANY_DECIMALS = 1.999
        temp_product = Product(name='Temporary', price=PRICE_TOO_MANY_DECIMALS, available=True)
        with self.assertRaises(ValidationError):
            temp_product.full_clean()

class CustomerModelTest(TestCase):
    def test_create_customer_with_valid_data(self):
        temp_customer = Customer.objects.create(name='John Doe', address='123 Main St')
        self.assertEqual(temp_customer.name, 'John Doe')
        self.assertEqual(temp_customer.address, '123 Main St')

    def test_create_customer_with_missing_name(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer(name='', address='123 Main St')
            temp_customer.full_clean()

    def test_create_customer_with_missing_address(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer(name='John Doe', address='')
            temp_customer.full_clean()

    def test_create_customer_with_blank_name(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer(name='', address='123 Main St')
            temp_customer.full_clean()

    def test_create_customer_with_blank_address(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer(name='John Doe', address='')
            temp_customer.full_clean()

    def test_create_customer_with_border_name_length(self):
        NAME_BORDER_LONG = 'a' * 100
        temp_customer = Customer.objects.create(name=NAME_BORDER_LONG, address='123 Main St')
        self.assertEqual(temp_customer.name, NAME_BORDER_LONG)


class OrderModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name='John Doe', address='123 Main St')
        self.product1 = Product.objects.create(name='Product 1', price=10.00, available=True)
        self.product2 = Product.objects.create(name='Product 2', price=20.00, available=False)

    def test_create_order_with_valid_data(self):
        order = Order.objects.create(customer=self.customer, status=OrderStatus.NEW)
        order.products.add(self.product1, self.product2)
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.status, OrderStatus.NEW)
        self.assertIn(self.product1, order.products.all())
        self.assertIn(self.product2, order.products.all())

    def test_create_order_with_missing_customer(self):
        order = Order(status=OrderStatus.NEW)
        with self.assertRaises(ValidationError):
            order.full_clean()
            order.save()

    def test_create_order_with_invalid_status(self):
        with self.assertRaises(ValidationError):
            order = Order.objects.create(customer=self.customer, status='INVALID_STATUS')
            order.full_clean()

    def test_total_price_calculation_with_valid_products(self):
        order = Order.objects.create(customer=self.customer, status=OrderStatus.NEW)
        order.products.add(self.product1, self.product2)
        self.assertEqual(order.calculate_total_price(), 30.00)

    def test_total_price_calculation_with_no_products(self):
        order = Order.objects.create(customer=self.customer, status=OrderStatus.NEW)
        self.assertEqual(order.calculate_total_price(), 0.00)

    def test_availability_order_with_all_products_available(self):
        order = Order.objects.create(customer=self.customer, status=OrderStatus.NEW)
        order.products.add(self.product1)
        self.assertTrue(order.availability_order())

    def test_availability_order_with_some_products_unavailable(self):
        order = Order.objects.create(customer=self.customer, status=OrderStatus.NEW)
        order.products.add(self.product1, self.product2)
        self.assertFalse(order.availability_order())
