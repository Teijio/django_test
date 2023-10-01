import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from robots.models import Robot

from .forms import OrderForm
from .models import Order


@csrf_exempt
def add_order(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        form = OrderForm(data)

        if form.is_valid():
            robot_serial = form.cleaned_data["robot_serial"]

            if Robot.objects.filter(serial=robot_serial).exists():
                form.save()
                return JsonResponse({"message": "Order added successfully"})
            else:
                Order.objects.create(
                    customer=form.cleaned_data["customer"],
                    robot_serial=robot_serial,
                    waiting_for_robot=True,
                )
                return JsonResponse(
                    {"message": "Robot with this serial does not exist."},
                    status=400,
                )
        else:
            return JsonResponse({"message": "Data is not correct"}, status=400)
