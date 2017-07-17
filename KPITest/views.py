from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
import datetime
from KPITest.forms import TaskCreateForm
from KPITest.helper import is_director
from KPITest.models import Employee, Department, Task, Report, TaskContext


@login_required
def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    employee = user.employee
    if request.user.employee.can_watch_page(employee):
        return render(request, 'KPITest/profile.html', {'employee': employee})
    else:
        return HttpResponseForbidden()  # return 403(access is denied) error


@login_required
def stats(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    employee = user.employee
    if request.user.employee.can_watch_page(employee):
        users_tasks = employee.tasks.all()
        return render(request, 'KPITest/stats.html', {'tasks': users_tasks})
    else:
        return HttpResponseForbidden()


@is_director(login_url=HttpResponseForbidden)
@login_required
def employees(request):
    user = request.user
    employee = user.employee
    if employee.departments_d.all().exists():
        departments = employee.departments_d.all()
        return render(request, 'KPITest/employees.html', {'current_employee': employee, 'department': departments})
    else:
        return HttpResponseForbidden()  # return 403(access is denied) error


@login_required
def tasks(request):
    employee = request.user.employee
    task_list = list()
    for t in employee.tasks.all():
        task_list.append(t)
    for d in employee.departments_d.all():
        for t in d.tasks.all():
            if not t.is_distributed():
                task_list.append(t)
    return render(request, 'KPITest/tasks.html', {'task_list': task_list})


@is_director(login_url=HttpResponseForbidden)
@login_required
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


@login_required
def report(request, report_id):
    rep = get_object_or_404(Report, pk=report_id)
    if request.user.employee.can_watch_task(rep.owner):
        return render(request, 'KPITest/report.html', {'rep': rep})
    else:
        return HttpResponseForbidden()


@login_required
def reports_list(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.user.employee.can_watch_task(task):
        reports = task.get_all_reports()
        return render(request, 'KPITest/reports-list.html', {'reports': reports})
    else:
        return HttpResponseForbidden()


def redirect_to_login_page(request):
    return redirect('auth')


@login_required
def log_out(request):
    logout(request)
    return redirect('auth')


#
#
# @is_director
# @login_required
# def create_task(request):
#     if request.method == 'POST':
#         form = TaskCreateForm(request.POST)
#         if form.is_valid():
#             task = form.save(commit=False)
#             task.employee = request.user.employee
#             #print(str(task.employee.user.user_name))
#             task.save()
#             return redirect(request,'tasks')
#     else:
#         form = TaskCreateForm()
#     return render(request, 'KPITest/create-task.html', {'form': form, "tcs": TaskContext.objects.all()})



@login_required
def create_task(request):
    if request.method == 'POST':
        count = request.POST['count']
        date = request.POST['date']
        task = request.POST['task']
        context = TaskContext.objects.get(pk=task)
        new_task = Task.objects.create(
            description=context.name,
            context=context,
            count=count,
            date=date,
            employee=request.user.employee
        )
        return redirect(request, 'tasks')
    else:
        return render(request, 'KPITest/create-task.html', {"tcs": TaskContext.objects.all()})


@login_required
def execute_task(request, task_id):
    if request.method == 'POST':
        employee = request.user.employee
        report_name = request.POST['report-name']
        description = request.POST['to-do']
        textarea = request.POST['textarea']
        # WTF ?!??!?!
        file = request.POST['file']


        report = Report.objects.create(
            owner=employee
##            done_count
        )

    else:
        return render(request, 'KPITest/execute.html', {"task_id": task_id})