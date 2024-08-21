from django.urls import path
from .views import login_view, register_view, logout_view, select_view

urlpatterns = [
    path('', select_view, name='select'),  # New select view as the main page
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]
