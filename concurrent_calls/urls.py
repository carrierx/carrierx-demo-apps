from django.urls import path
from . import views

urlpatterns = [
    path('', views.concurrent_calls),
]
