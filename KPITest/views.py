from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from KPITest.models import Employee, Department, Task


@login_required(login_url='/auth')
def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    employee = get_object_or_404(Employee, user=user)
    if employee.can_watch_page(request.user):
        return render(request, 'KPITest/profile.html', {'employee': employee})
    else:
        return HttpResponseForbidden()  # return 403(access is denied) error


@login_required(login_url='/auth')
def stats(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    employee = get_object_or_404(Employee, user=user)
    if employee.can_watch_page(request.user):
        users_tasks = employee.view_my_tasks()
        return render(request, 'KPITest/stats.html', {'tasks': users_tasks})
    else:
        return HttpResponseForbidden()


@login_required(login_url='/auth')
def employees(request):
    user = request.user
    employee = get_object_or_404(Employee, user=user)
    if employee.is_director():
        departments = employee.controlled_departments()
        return render(request, 'KPITest/employees.html', {'current_employee': employee, 'department': departments})
    else:
        return HttpResponseForbidden()  # return 403(access is denied) error


@login_required(login_url='/')
def tasks(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    employee = get_object_or_404(Employee, user=user)
    if user == request.user:
        context = {
            'tasks': employee.view_my_tasks()
        }
        return render(request, 'KPITest/personal_tasks.html', context)
    else:
        return HttpResponseForbidden()  # return 403(access is denied) error


@login_required(login_url='/auth')
def employees_tasks(request):
    user = request.user
    director = get_object_or_404(Employee, user=user)
    if director.is_director():
        departments = get_list_or_404(Department, derectors=director)
        employees = departments.employees.distinct()
        tasks = get_list_or_404(Task, owner=employees)
        context = {
            'tasks': tasks
        }
        return render(request, 'KPITest/employees_tasks.html', context)  # Прописать правильно
    else:
        return HttpResponseForbidden()


def redirect_to_login_page(request):
    return redirect('auth')
