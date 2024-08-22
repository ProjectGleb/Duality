from django.contrib import admin
from .models import Project, Task

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    search_fields = ('name', 'user__username')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'project_user', 'created_at', 'success_rate', 'execution_count')
    list_filter = ('project', 'created_at')
    search_fields = ('name', 'description', 'project__user__username')

    def project_user(self, obj):
        return obj.project.user
    project_user.short_description = 'User'

admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)