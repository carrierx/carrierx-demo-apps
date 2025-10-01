from django.urls import path
from . import views

app_name = "vcon"
urlpatterns = [
    path("", views.route, name="vcon-start"),
    path("end/", views.end, name="vcon-end"),
]
