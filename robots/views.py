import json
from datetime import datetime

from django.conf import settings
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openpyxl import Workbook

from .forms import RobotForm
from .models import Robot

LAST_SEVEN_DAYS = settings.LAST_SEVEN_DAYS


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


def get_data_for_time_period(time_period: datetime) -> dict:
    data = (
        Robot.objects.filter(created__gte=time_period)
        .values("model", "version")
        .annotate(count=Count("version"))
        .order_by("model", "version")
    )

    grouped_data = {}

    for result in data:
        model = result["model"]
        version = result["version"]
        count = result["count"]

        if model not in grouped_data:
            grouped_data[model] = []

        grouped_data[model].append((model, version, count))

    return grouped_data


def export_data_to_excel(data: dict) -> Workbook:
    wb = Workbook()
    headers = ("Модель", "Версия", "Количество за неделю")
    for model, records in data.items():
        ws = wb.create_sheet(title=model)
        ws.append(headers)

        for record in records:
            ws.append(record)

    del wb["Sheet"]

    return wb


def download_excel(request):
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = 'attachment; filename="products.xlsx"'

    data = get_data_for_time_period(LAST_SEVEN_DAYS)
    if not data:
        return JsonResponse(
            {"message": "No data available for the last seven days"},
            status=400,
        )

    wb = export_data_to_excel(data)
    wb.save(response)
    return response
