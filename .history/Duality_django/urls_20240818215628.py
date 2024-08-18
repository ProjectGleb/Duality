"""
URL configuration for Duality_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

#MY IMPORT OF AUTHNETICATION APP
from authentication import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),  #if user serches /authentication/ url, it will redirect django to look into authentication.urls folder
    path('', include('authentication.urls')),  #if user serches / url, it will redirect django to look into authentication.urls folder
    path('home/', include('home.urls')),  #if user serches / url, it will redirect django to look into authentication.urls folder
    path('projects/', include('projects.urls')),  #if user serches / url, it will redirect django to look into authentication.urls folder
    path('discover/', include('discover.urls')),  #if user serches / url, it will redirect django to look into authentication.urls folder
    path('settings/', include('settings_page.urls')),  #if user serches / url, it will redirect django to look into authentication.urls folder
]
