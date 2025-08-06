from django.urls import path
from . import views

urlpatterns = [
    path("totem/", views.validador, name="totem")
]
