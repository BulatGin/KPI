from django.contrib.auth.models import User
from django.db import models


class Employee(models.User):
    patronymic = models.CharField(max_length=30, blank=True)  # Отчество
    age = models.IntegerField(default=0)
    photo = models.ImageField(blank=True)
    position = models.CharField(max_length=30)
    is_director = models.BooleanField()
    parent = models.ForeignKey('self')
    department_name = models.CharField(max_length=40, blank=True)
    employees = models.ManyToManyField('User')


class Task(models.Model):
    parent = models.ForeignKey('self')  # Т.к. задача дробится (на другие задачи), задача содержит ссылку на родителя
    owner = models.ForeignKey(models.Employee)
    name = models.CharField(max_length=40)
    description = models.TextField()
    report = models.TextField(blank=True)  # Не формируется на вышестоящих уровнях
    count = models.IntegerField(default=0)
    done_count = models.IntegerField(default=0)
    date = models.DateField()
    state = models.BooleanField()  # 0 - задача не распределена, 1 - задача распределена
