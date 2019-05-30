from django.urls import path
from . import views

urlpatterns = [
    path("", views.start, name="start"),
    path("goodbye/", views.say_goodbye, name="say_goodbye"),
    path("send/", views.send, name="send")
]
