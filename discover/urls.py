from django.urls import path
from . import views

urlpatterns = [
    path('', views.discover_view, name='discover'),
]