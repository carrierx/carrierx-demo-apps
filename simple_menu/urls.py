from django.urls import path
from . import views

app_name = "simple_menu"
urlpatterns = [
    path("", views.start, name="main"),
    path("redirect/", views.redirect, name="redirect"),
]
