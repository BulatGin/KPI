from django.contrib import admin
from KPITest.models import Employee, Position, Department, Task, TaskType

admin.site.register(Employee)
admin.site.register(Position)
admin.site.register(Department)
admin.site.register(Task)
admin.site.register(TaskType)
