from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.shortcuts import render, get_object_or_404

from KPITest.models import Employee, Department, Task


def profile(request, user_id):
    pass


def stats(request, user_id):
    pass


def employees(request):
    pass


@login_required(login_url='/')
def tasks(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    employee = get_object_or_404(Employee, user=user)
    context = {
        'tasks': Employee.view_my_tasks(employee)
    }
    return render(request, 'personal_tasks.html', context)  # Прописать правильно


@login_required(login_url='/')
def employees_tasks(request):
    user = get_object_or_404(User, pk=request.user)
    director = get_object_or_404(Employee, user=user)
    departments = Department.objects.filter(directors__contains=director)
    employees = departments.employees.distinct()
    tasks = Task.objects.filter(owner__in=employees)
    context = {
        'tasks': tasks
    }
    return render(request, 'employees_tasks.html', context)  # Прописать правильно

