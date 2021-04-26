from django.urls import path
from . import views

app_name = "catalog"
urlpatterns = [
    path("", views.main, name="main"),
    path("<slug:flexiapp_name>/", views.detail, name="detail"),
]
