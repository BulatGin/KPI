from django.contrib.auth.models import User
from django.db import models


class Department(models.Model):
    parent = models.ForeignKey('self')
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=40, blank=True)
    employees = models.ManyToManyField(Employee)
    directors = models.ManyToManyField(Employee)

    def controlled_departments(self):
        return Department.objects.filter(parent=self)


class Position(models.Model):
    name = models.CharField(max_length=15)


class Employee(models.Model):
    user = models.OneToOneField(User)
    middle_name = models.CharField(max_length=30, blank=True)  # Отчество
    age = models.IntegerField(default=0)
    photo = models.ImageField(blank=True)
    position = models.ManyToManyField(Position)

    def is_director(self):
        return Department.objects.filter(directors=self).exists()

    def my_departments(self):
        return Department.objects.filter(employees=self)

    def controlled_departments(self):
        return Department.objects.filter(directors=self)

    def can_watch_page(self, user):
        if self == user:
            return True
        else:
            departments = Department.objects.filter(employees=self)
            while True:
                if user in departments.directors:
                    return True
                dep_parent = department.parent
                if dep_parent is None:
                    break
                else:
                    department = dep_parent
            return False

    def view_my_tasks(self):
        return Task.objects.filter(owner=self)

    # task - тот, который распределяют, tasks - dict, key - пользователь, которому распределена задача, value - кол-во
    def distribute(self, task, tasks):
        for key, value in tasks:
            mini_task = Task.objects.create(owner=key, name=task.name, description=task.description,
                                            count=value, date=task.date, type=task.type)
            if Employee.is_director(key):
                mini_task.state = False
            else:
                mini_task.state = True
            mini_task.save()


class Task(models.Model):
    owner = models.ForeignKey(Employee)
    name = models.CharField(max_length=40)
    description = models.TextField(blank=True)
    count = models.IntegerField(default=0)
    done_count = models.IntegerField(default=0)
    date = models.DateField()
    state = models.BooleanField()  # 0 - задача не распределена, 1 - задача распределена
    type = models.ForeignKey(TaskType)


class TaskType(models.Model):
    type = models.CharField(max_length=10)


class Report(models.Model):
    owner = models.ForeignKey(Task)
    done_count = models.IntegerField(default=0)
    name = models.CharField(max_length=15)
    description = models.TextField()


class File(models.Model):
    owner = models.ForeignKey(Report)
    file = models.FileField()
