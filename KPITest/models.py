from django.contrib.auth.models import User
from django.db import models


class Department(models.Model):
    parent = models.OneToOneField('Department')
    name = models.CharField(max_length=40)


class UserAndDepartmentConnection(models.Model):
    user = models.ForeignKey(User)
    department = models.ForeignKey(Department)


class Task(models.Model):
    parent = models.OneToOneField('Task')
    name = models.CharField(max_length=40)
    description = models.TextField()
    count = models.IntegerField(default=0)
    date = models.DateField()


class DepartmentAndTaskConnection(models.Model):
    department = models.ForeignKey(Department)
    task = models.ForeignKey(Task)
    KPI = models.FloatField(default=0.0)


class UserAndTaskConnection(models.Model):
    user = models.ForeignKey(User)
    task = models.ForeignKey(Task)
    KPI = models.FloatField(default=0.0)


class DepartmentAndBossConnection(models.Model):
    boss = models.ForeignKey(User)
    department = models.ForeignKey(Department)



