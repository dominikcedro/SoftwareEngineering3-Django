from django.shortcuts import render
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from decimal import Decimal

# Create your views here.
def hello_world(request):
    return HttpResponse("Hello world")

@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        products = list(Product.objects.values('id', 'name', 'price', 'available'))
        return JsonResponse(products, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        price = data.get('price')
        available = data.get('available')
        product = Product(name=name, price=Decimal(str(price)), available=available)
        product.full_clean()
        product.save()
        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'available': product.available
        }, status=201
        )
@csrf_exempt
def product_detail(request, product_id):
    if request.method == 'GET':
        product = Product.objects.get(id=product_id)
        return JsonResponse({
            'id':product.id,
            'name': product.name,
            'price': float(product.price),
            'available': product.available
            }
        )