from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects_view, name='projects'),
    path('tasks/<int:project_id>/', views.get_tasks, name='get_tasks'),
]