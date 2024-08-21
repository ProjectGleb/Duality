from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def settings_page(request):
    return render(request, 'settings_page.html')
