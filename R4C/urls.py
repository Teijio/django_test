from django.contrib import admin
from django.urls import path

from robots.views import add_robot, download_excel

urlpatterns = [
    path("admin/", admin.site.urls),
    path("add_robot/", add_robot),
    path("download_excel/", download_excel),
]
