from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
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
    departments = employee.departments_d.all()
    return render(request, 'KPITest/employees.html', {'current_employee': employee, 'departments': departments})



@login_required
def tasks(request):
    employee = request.user.employee
    return render(request, 'KPITest/tasks.html', {'tasks': employee.tasks.all()})


@is_director(login_url=HttpResponseForbidden)
@login_required
def employees_tasks(request):
    user = request.user
    director = user.employee
    departments = director.departments_d.all()
    departments_tasks = []
    subordinates_tasks = []
    for department in departments:
        for task in department.tasks.all():
            if not task.is_distributed():
                departments_tasks.append(task)
            for child_task in task.children.all():
                subordinates_tasks.append(child_task)
    return render(request, 'KPITest/employees_tasks.html', {'departments_tasks': departments_tasks, 'subordinates_tasks': subordinates_tasks})


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
        new_task = Task(parent=task, description=request.POST['description'],
                        parent_id=task.id, context=task.context, count=int(request.POST['count']),
                        date=request.POST['date'])
        if int(request.POST['count']) + task.get_distributed_count() > task.count:
            error = 'Вы не можете распределить больше {0} заданий'.format(task.get_not_distributed_count())
        elif dep_id is '' and emp_id is not '':
            new_task.employee = Employee.objects.get(pk=emp_id)
            new_task.save()
        elif dep_id is not '' and emp_id is '':
            new_task.department = Department.objects.get(pk=dep_id)
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


def redirect_to_login_page(request):
    return redirect('auth')


@login_required
def log_out(request):
    logout(request)
    return redirect('auth')
