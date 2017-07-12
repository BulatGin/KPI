from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, get_list_or_404

from KPITest.models import Employee, Task


def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    employee = get_object_or_404(Employee, user=user)
    if employee.can_watch_page(request.user):
        return render(request, 'KPITest/profile.html', {'employee': employee})
    else:
        return HttpResponseForbidden()  # return 403(access is denied) error


def stats(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    employee = get_object_or_404(Employee, user=user)
    if employee.can_watch_page(request.user):
        users_tasks = employee.view_my_tasks()
        return render(request, 'KPITest/stats.html', {'tasks': users_tasks})
    else:
        return HttpResponseForbidden()  # return 403(access is denied) error


def employees(request):
    user = request.user
    employee = get_object_or_404(Employee, user=user)
    if employee.is_director():
        department = employee.department_set
        return render(request, 'KPITest/employees.html', {'current_employee': employee, 'department': department})
    else:
        return HttpResponseForbidden()  # return 403(access is denied) error
