from django.urls import path
from . import views

app_name = "routing_engine"
urlpatterns = [
    path("", views.route, name="route"),
]
