from django.contrib import admin
from django.urls import path

from robots.views import add_robot, download_excel
from orders.views import add_order

urlpatterns = [
    path("admin/", admin.site.urls),
    path("add_robot/", add_robot),
    path("add_order/", add_order),
    path("download_excel/", download_excel),
]
