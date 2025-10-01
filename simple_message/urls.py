from django.urls import path
from . import views

urlpatterns = [
    path("", views.simple_message),
    path("digits/", views.digits, name="digits")
]
