from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def projects_view(request):
    return render(request, 'projects.html')  # Adjust the path to your HTML file accordingly
