from django.urls import path
from . import views

urlpatterns = [
    path("", views.forward, name="start"),
]
