from django.contrib.auth.models import User
from django.db import models


class Employee(models.User):
    is_director = models.BooleanField()
    parent = models.OneToOneField('self')
    department_name = models.CharField(max_length=40)
    employees = models.ManyToManyField('User')


class Task(models.Model):
    parent = models.OneToOneField('Task')  # Т.к. задача дробится (на другие задачи), задача содержит ссылку на родителя
    owner = models.ForeignKey(models.Employee)  # Задача может принадлежать или отделу, или сотруднику
    name = models.CharField(max_length=40)
    description = models.TextField()
    report = models.TextField()  # Не формируется на вышестоящих уровнях
    count = models.IntegerField(default=0)
    date = models.DateField()
    state = models.BooleanField()
    KPI = models.FloatField(default=0.0)
