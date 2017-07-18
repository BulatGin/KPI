from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from KPITest.helper import is_director, can_watch_page
from KPITest.models import Employee, Department, Task, Report, TaskContext, File


@login_required
@can_watch_page
def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    employee = user.employee
    return render(request, 'KPITest/profile.html', {'employee': employee})


@login_required
@can_watch_page
def stats(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    employee = user.employee
    users_tasks = employee.tasks.all()
    return render(request, 'KPITest/stats.html', {'tasks': users_tasks})


@login_required
@is_director
def employees(request):
    user = request.user
    employee = user.employee
    departments = employee.departments_d.all()
    return render(request, 'KPITest/employees.html', {'current_employee': employee, 'departments': departments})


@login_required
def tasks(request):
    employee = request.user.employee
    return render(request, 'KPITest/tasks.html', {'tasks': employee.tasks.all()})


@login_required
@is_director
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
@can_watch_page
def reports_list(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'KPITest/reports-list.html', {'task': task})


@login_required
@is_director
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
        return redirect('tasks')
    else:
        return render(request, 'KPITest/create-task.html', {"tcs": TaskContext.objects.all()})


@login_required
def execute_task(request, task_id):
    if request.method == 'POST':
        employee = request.user.employee
        report_name = request.POST['report-name']
        description = request.POST['to-do']
        textarea = request.POST['textarea']

        report = Report.objects.create(
            owner=get_object_or_404(Task, pk=task_id),
            done_count=description,
            name=report_name,
            description=textarea,
        )

        post_file = request.FILES['file']
        file = File.objects.create(
            file=post_file,
            owner=report,
        )

        return redirect('tasks')

    else:
        return render(request, 'KPITest/execute.html', {"task_id": task_id})


def redirect_to_login_page(request):
    return redirect('auth')


@login_required
def log_out(request):
    logout(request)
    return redirect('auth')
