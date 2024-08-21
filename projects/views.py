from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from home.models import Project, Task 
from django.http import JsonResponse

def projects_view(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'projects.html', {'projects': projects})

def get_tasks(request, project_id):
    tasks = Task.objects.filter(project_id=project_id)
    tasks_data = list(tasks.values('id', 'name', 'description', 'steps', 'success_rate'))
    print(f"Returning {len(tasks_data)} tasks for project {project_id}")  # Add this line for debugging
    return JsonResponse(tasks_data, safe=False)