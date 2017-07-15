from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from KPITest.helper import is_director
from KPITest.models import Employee, Department, Task, Report


@login_required(login_url='/auth')
def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    employee = user.employee
    if request.user.employee.can_watch_page(employee):
        return render(request, 'KPITest/profile.html', {'employee': employee})
    else:
        return HttpResponseForbidden()  # return 403(access is denied) error


@login_required(login_url='/auth')
def stats(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    employee = user.employee
    if request.user.employee.can_watch_page(employee):
        users_tasks = employee.tasks.all()
        return render(request, 'KPITest/stats.html', {'tasks': users_tasks})
    else:
        return HttpResponseForbidden()


@is_director(login_url=HttpResponseForbidden)
@login_required(login_url='/auth')
def employees(request):
    user = request.user
    employee = user.employee
    if employee.departments_d.all().exists():
        departments = employee.departments_d.all()
        return render(request, 'KPITest/employees.html', {'current_employee': employee, 'department': departments})
    else:
        return HttpResponseForbidden()  # return 403(access is denied) error


@login_required(login_url='/auth')
def tasks(request):
    employee = request.user.employee
    task_list = list()
    for t in employee.tasks.all():
        task_list.append(t)
    for d in employee.departments_d.all():
        for t in d.tasks.all():
            if not t.is_distributed():
                task_list.append(t)
    return render(request, 'KPITest/tasks.html', 'task_list': task_list)


@is_director(login_url=HttpResponseForbidden)
@login_required(login_url='/auth')
def employees_tasks(request):
    user = request.user
    director = user.employee
    if director.is_director():
        task_list = list()
        for d in director.departments_d.all():
            for t in d.tasks.all():
                for m in t.children.all():
                    task_list.append(m)
        return render(request, 'KPITest/employees_tasks.html', {'task_list': task_list})
    else:
        return HttpResponseForbidden()


@login_required(login_url='/auth')
def report(request, report_id):
    rep = get_object_or_404(Report, pk=report_id)
    if request.user.employee.can_watch_task(rep.owner):
        return render(request, 'KPITest/report.html', {'rep': rep})
    else:
        return HttpResponseForbidden()


@login_required(login_url='/auth')
def report_list(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.user.employee.can_watch_task(task):
        reports = task.get_all_reports()
        return render(request, 'KPITest/reports-list.html', {'reports': reports})
    else:
        return HttpResponseForbidden()


def redirect_to_login_page(request):
    return redirect('auth')


@login_required(login_url='/auth')
def log_out(request):
    logout(request)
    return redirect('auth')
