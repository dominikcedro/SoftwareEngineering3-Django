# myproject/myapp/views.py
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Product
import json

@csrf_exempt
@require_http_methods(["GET", "POST"])
def product_list(request):
    if request.method == "GET":
        products = Product.objects.all().values()
        return JsonResponse(list(products), safe=False)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")

        if not all(key in data for key in ("name", "price", "available")):
            return HttpResponseBadRequest("Missing necessary fields")

        if data["price"] <= 0:
            return HttpResponseBadRequest("Price must be positive")

        try:
            product = Product.objects.create(
                name=data["name"],
                price=data["price"],
                available=data["available"]
            )
        except ValidationError as e:
            return HttpResponseBadRequest(str(e))

        return JsonResponse(
            {"id": product.id, "name": product.name, "price": product.price, "available": product.available},
            status=201)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponseNotFound("Product not found")

    if request.method == "GET":
        return JsonResponse(
            {"id": product.id, "name": product.name, "price": product.price, "available": product.available})

    if request.method == "PUT":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")

        if not all(key in data for key in ("name", "price", "available")):
            return HttpResponseBadRequest("Missing necessary fields")

        if data["price"] <= 0:
            return HttpResponseBadRequest("Price must be positive")

        try:
            product.name = data["name"]
            product.price = data["price"]
            product.available = data["available"]
            product.save()
        except ValidationError as e:
            return HttpResponseBadRequest(str(e))

        return JsonResponse(
            {"id": product.id, "name": product.name, "price": product.price, "available": product.available})

    if request.method == "DELETE":
        product.delete()
        return JsonResponse({"message": "Product deleted successfully"}, status=204)