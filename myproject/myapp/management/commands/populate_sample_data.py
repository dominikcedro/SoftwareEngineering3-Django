# myproject/myapp/management/commands/populate_sample_data.py
from django.core.management.base import BaseCommand
from myapp.models import Product, Customer, Order, OrderStatus

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Product.objects.all().delete()
        # Customer.objects.all().delete()
        # Order.objects.all().delete()

        product1 = Product.objects.create(
            name="testing1_product",
            price=19.99,
            available=True
        )

        customer1 = Customer.objects.create(
            name="testing1name",
            address="testing1_address"
        )

        order1 = Order.objects.create(
            customer=customer1,
            status=OrderStatus.NEW
        )

        order1.products.add(product1)
        self.stdout.write("Data created successfully.")