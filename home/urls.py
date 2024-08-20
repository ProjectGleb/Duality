from django.urls import path
from . import views
from . import views_record

urlpatterns = [
    path('', views.home_view, name='home'),
    path('process_input/', views.process_input, name='process_input'),
    path('recording_start/', views_record.recording_start, name='recording_start'),
    path('recording_end/', views_record.recording_end, name='recording_end'),
]