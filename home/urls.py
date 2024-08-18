from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('process_input/', views.process_input, name='process_input'),
]

