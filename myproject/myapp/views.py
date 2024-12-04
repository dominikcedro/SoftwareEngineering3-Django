from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer
import json

@csrf_exempt
@require_http_methods(["GET", "POST"])
def customer_list(request):
    if request.method == "GET":
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")

        serializer = CustomerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return HttpResponseBadRequest(serializer.errors)

@csrf_exempt
@require_http_methods(["GET"])
def customer_detail(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return HttpResponseNotFound("Customer not found")

    serializer = CustomerSerializer(customer)
    return JsonResponse(serializer.data)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def order_list(request):
    if request.method == "GET":
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")

        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return HttpResponseBadRequest(serializer.errors)

@csrf_exempt
@require_http_methods(["GET"])
def order_detail(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return HttpResponseNotFound("Order not found")

    serializer = OrderSerializer(order)
    return JsonResponse(serializer.data)