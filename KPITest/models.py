from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Department(models.Model):
    parent = models.ForeignKey('self', related_name='children', blank=True, null=True)
    name = models.CharField(max_length=40, verbose_name='Название')
    address = models.CharField(max_length=80, blank=True, null=True, verbose_name='Адрес')
    employees = models.ManyToManyField('Employee', related_name='departments_e', verbose_name='Сотрудники')
    directors = models.ManyToManyField('Employee', related_name='departments_d', verbose_name='Руководители')

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=50, verbose_name='Должность')

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(User)
    middle_name = models.CharField(max_length=30, blank=True, null=True, verbose_name='Отчество')  # Отчество
    age = models.IntegerField(default=0, verbose_name='Возраст', validators=[MinValueValidator(0),
                                                                             MaxValueValidator(100)])
    photo = models.ImageField(blank=True, null=True, verbose_name='Фото', upload_to='img/')
    position = models.ManyToManyField('Position', related_name='employees', verbose_name='Должности')

    def __str__(self):
        return self.user.username

    def is_director(self):
        return self.departments_d.all().exists()

    #  Проверяет, можно ли пользователю просматривать страницу (может он сам и его начальники)
    #  Смысл: self пытается посмотреть страницу employee
    def can_watch_page(self, employee):
        if self == employee:
            return True
        else:
            for d in employee.departments_e.all():
                while True:
                    if d.directors.filter(user=self.user).exists():
                        return True
                    dep_parent = d.parent
                    if dep_parent is None:
                        break
                    else:
                        d = dep_parent
            return False

    #  Может ли человек просматривать задание (т.к. task может не иметь ссылки на employee, зато иметь на department)
    def can_watch_task(self, task):
        if task.employee == self:
            return True
        else:
            if task.department is None:
                return self.can_watch_page(task.employee)
            else:
                d = task.department
                while True:
                    if d.directors.filter(user=self.user).exists():
                        return True
                    dep_parent = d.parent
                    if dep_parent is None:
                        break
                    else:
                        d = dep_parent

    # Распределение заданий
    # task - тот, который распределяют, tasks - dict, key - пользователь, которому распределена задача, value - кол-во
    def distribute(self, task, tasks):
        for key, value in tasks:
            mini_task = Task.objects.create(owner=key, name=task.name, description=task.description,
                                            count=value, date=task.date, type=task.type)
            if key.departments_d.all().exists():  # Если задание пришло директору, то статус "Не распределено"
                mini_task.state = False
            else:  # Если конечному сотруднику, то "Распределено"
                mini_task.state = True
            mini_task.save()


class Task(models.Model):
    #  Задача принадлежит или сотруднику, или отделу
    employee = models.ForeignKey('Employee', related_name='tasks', verbose_name='Поручено (сотрудник)', blank=True,
                                 null=True)
    department = models.ForeignKey('Department', related_name='tasks', verbose_name='Поручено (отдел)', blank=True,
                                   null=True)
    parent = models.ForeignKey('Task', related_name='children', blank=True, null=True)

    name = models.CharField(max_length=40, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    count = models.IntegerField(default=0, verbose_name='Кол-во', validators=[MinValueValidator(0)])
    date = models.DateField(verbose_name='Дата конца')
    type = models.ForeignKey('TaskType', verbose_name='Тип задания')

    def __str__(self):
        return self.name

    def get_distributed_count(self):
        count = 0
        for t in self.children.all():
            count += t.count
        return count

    def is_distributed(self):
        return str(self.count) == str(self.get_distributed_count())

    #  Рекурсивно получает кол-во выполненных заданий
    def get_done_count(self):
        count = self.get_done_count_from_reports()
        for t in self.children.all():
            count += t.get_done_count()
        return count

    #  Вспомогательный метод для метода выше
    def get_done_count_from_reports(self):
        count = 0
        for r in self.reports.all():
            count += r.done_count
        return count

    #  Рекурсивно получает все отчёты
    def get_all_reports(self):
        rep_set = set()
        for r in self.reports.all():
            rep_set.add(r)
        for t in self.children.all():
            rep_set.update(t.get_all_reports())
        return rep_set


class TaskType(models.Model):
    type = models.CharField(max_length=40)

    def __str__(self):
        return self.type


class Report(models.Model):
    owner = models.ForeignKey('Task', related_name='reports', verbose_name='Задание')
    done_count = models.IntegerField(default=0, verbose_name='Сделано', validators=[MinValueValidator(0)])
    name = models.CharField(max_length=40, verbose_name='Название')
    description = models.TextField(verbose_name='Отчёт')

    def __str__(self):
        return self.name


class File(models.Model):
    owner = models.ForeignKey('Report', related_name='files', verbose_name='Отчёт')
    file = models.FileField(verbose_name='Файл', upload_to='files/')
