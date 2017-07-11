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
    user = User  # ?????
    middle_name = models.CharField(max_length=30, blank=True)  # Отчество
    age = models.IntegerField(default=0)
    photo = models.ImageField(blank=True)

    position = models.ManyToManyField(Position)
    department = models.ForeignKey(Department)

    def controlled_departments(self):
        return Department.objects.filter(self in Department.directors)

    def can_watch_page(self, user):
        if self == user:
            return True
        else:
            department = user.department
            while True:
                if user in department.directors:
                    return True
                dep_parent = department.parent
                if dep_parent is None:
                    break
                else:
                    department = dep_parent
            return False

    def view_my_tasks(self):
        return Task.objects.filter(owner=self)

    def distribute(self, task, tasks):
        pass  # TODO


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
