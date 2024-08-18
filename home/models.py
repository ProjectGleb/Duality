from django.db import models
from django.contrib.auth.models import User  # Import the built-in User model

class UserProject(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class UserTask(models.Model):
    project = models.ForeignKey(UserProject, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    success_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} (Project: {self.project.title})"
    
    
# EXPLANATION 

# UserProject:
# title: The name of the project.
# description: Optional text field to describe the project.
# user: A foreign key to the User model, indicating that each project belongs to a user. The on_delete=models.CASCADE means that if a user is deleted, their associated projects will also be deleted.
# created_at: Automatically records when the project was created.
# UserTask:

# project: A foreign key to UserProject, indicating that each task is related to a project.
# title: The name of the task.
# description: Optional text field for more details about the task.
# created_at: Automatically records when the task was created.
# success_rate: A decimal field to record the success rate of the task (optional).