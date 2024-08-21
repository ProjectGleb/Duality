from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json

class Project(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    @property
    def task_count(self):
        return self.tasks.count()

class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    steps = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)
    success_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.name} (Project: {self.project.name})"

    def set_steps_from_json(self, json_file_path):
        with open(json_file_path, 'r') as file:
            self.steps = json.load(file)
        self.save()


# ------------------------------------------  Make a db for the discover page ------------------------------------------
    
    
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