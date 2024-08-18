from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects_view, name='project'),  # This will be the homepage after login
]

#PERHAPS MAKE ONE FOR THE TASKS PAGE ONCE THE PROJECT IS OPPENED
# urlpatterns = [
#     path('', views.home_view, name='view'),  # This will be the homepage after login
# ]
