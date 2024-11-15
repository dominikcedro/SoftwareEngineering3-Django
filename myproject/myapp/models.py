from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class OrderStatus(models.TextChoices): # i suppose this is a wat to create enums?
    NEW = 'NEW', 'New'
    IN_PROCESS = 'IN_PROCESS', 'In Process'
    SENT = 'SENT', 'Sent'
    COMPLETED = 'COMPLETED', 'Completed'

def validate_positive(value): # custom validation for part 5
    if value <= 0:
        raise ValidationError(
            _("%value)s is not positive"),
            params={"value: value"},
        )
class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, default=0, validators=[validate_positive])
    available = models.BooleanField(default=True)

class Customer(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=OrderStatus.choices)

    def calculate_total_price(self):
        return sum(product.price for product in self.products.all())

    def availability_order(self):
        return all(product.available for product in self.products.all())

