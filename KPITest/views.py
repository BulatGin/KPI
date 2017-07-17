from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from KPITest.helper import is_director
from KPITest.models import Employee, Department, Task, Report


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


@is_director(login_url=HttpResponseForbidden)
@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    error = ''
    if request.method == "POST":
        dep_id = request.POST['department']
        emp_id = request.POST['employee']
        if int(request.POST['count']) + task.get_distributed_count() > task.count:
            error = 'Вы не можете распределить больше {0} заданий'.format(task.get_not_distributed_count())
        elif dep_id is '' and emp_id is not '':
            employee = Employee.objects.get(pk=emp_id)
            new_task = Task(employee=employee, parent=task, description=request.POST['description'],
                            parent_id=task.id, context=task.context, date=task.date, count=int(request.POST['count']))
            new_task.save()
        elif dep_id is not '' and emp_id is '':
            department = Department.objects.get(pk=dep_id)
            new_task = Task(department=department, parent=task, description=request.POST['description'],
                            parent_id=task.id, context=task.context, date=task.date, count=int(request.POST['count']))
            new_task.save()
        else:
            error = 'Заполните ОДНО из полей: подразделение или сотрудник'
    department = task.department
    emp_list = Employee.objects.filter(departments_e=department)
    dep_list = Department.objects.filter(parent=department)
    if task.is_distributed():
        return redirect('/tasks/')
    return render(request, 'KPITest/add-task.html', {'emp_list': emp_list, 'dep_list': dep_list,
                                                     'err': error, 'task': task})


def create_task(request):
    pass


def execute_task(request):
    pass


def redirect_to_login_page(request):
    return redirect('auth')


@login_required
def log_out(request):
    logout(request)
    return redirect('auth')
