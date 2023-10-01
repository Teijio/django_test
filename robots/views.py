import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import RobotForm


@csrf_exempt
def add_robot(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        form = RobotForm(data)

        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Robot added successfully"})
        else:
            return JsonResponse({"message": "Data is not correct"}, status=400)
