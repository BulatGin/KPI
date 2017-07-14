from django.contrib.auth.models import User
from django.db import models


class Department(models.Model):
    parent = models.ForeignKey('self', related_name='children')
    name = models.CharField(max_length=40, verbose_name='Название')
    address = models.CharField(max_length=40, blank=True, verbose_name='Адрес')
    employees = models.ManyToManyField('Employee', related_name='departments_e', verbose_name='Сотрудники')
    directors = models.ManyToManyField('Employee', related_name='departments_d', verbose_name='Руководители')

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=15, verbose_name='Должность')

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    middle_name = models.CharField(max_length=30, blank=True, verbose_name='Отчество')  # Отчество
    age = models.IntegerField(default=0, verbose_name='Возраст')
    photo = models.ImageField(blank=True, verbose_name='Фото')
    position = models.ManyToManyField('Position', related_name='employees', verbose_name='Должности')

    def __str__(self):
        return self.user.first_name + self.user.last_name + self.middle_name

    #  Контролирует ли пользователь какой-либо отдел
    def is_director(self):
        return hasattr(self, 'departments_d')

    #  Возвращает отделы, в которых работает сотрудник
    def my_departments(self):
        if hasattr(self, 'departments_e'):
            return self.departments_e.all()
        else:
            return None

    #  Возвращает отделы, которые контролируются этим сотрудником
    def controlled_departments(self):
        if self.is_director():
            return self.departments_d.all()
        else:
            return None

    #  Проверяет, можно ли пользователю просматривать страницу (может он сам и его начальники)
    def can_watch_page(self, user):
        if self == user:
            return True
        else:
            departments = self.my_departments()
            if departments is not None:
                for d in departments:
                    while True:
                        if user in d.directors:
                            return True
                        dep_parents = d.parent
                        if dep_parents is None:
                            break
                        else:
                            d = dep_parents
            return False

    #  Возвращает все задания сотрудника
    def view_my_tasks(self):
        if hasattr(self, 'tasks'):
            return self.tasks.all()
        else:
            return None

    # Распределение заданий
    # task - тот, который распределяют, tasks - dict, key - пользователь, которому распределена задача, value - кол-во
    def distribute(self, task, tasks):
        for key, value in tasks:
            mini_task = Task.objects.create(owner=key, name=task.name, description=task.description,
                                            count=value, date=task.date, type=task.type)
            if Employee.is_director(key):  # Если задание пришло директору, то статус "Не распределено"
                mini_task.state = False
            else:  # Если конечному сотруднику, то "Распределено"
                mini_task.state = True
            mini_task.save()


class Task(models.Model):
    owner = models.ForeignKey('Employee', related_name='tasks', verbose_name='Поручено')
    parent = models.ForeignKey('Task', related_name='children')
    name = models.CharField(max_length=40, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    count = models.IntegerField(default=0, verbose_name='Кол-во')
    done_count = models.IntegerField(default=0, verbose_name='Сделано')
    date = models.DateField(verbose_name='Дата конца')
    state = models.BooleanField()  # 0 - задача не распределена, 1 - задача распределена
    type = models.ForeignKey('TaskType', verbose_name='Тип задания')

    def __str__(self):
        return self.name

    #  Рекурсивно получает кол-во выполненных заданий
    def get_all_count(self):
        count = self.done_count
        if hasattr(self, 'children'):
            mini_tasks = self.children.all()
            for t in mini_tasks:
                count += t.get_all_count()
            return count
        else:
            return count

    #  Рекурсивно получает все отчёты. Если отчётов нет, вернётся 1 элемент None
    def get_all_reports(self):
        l = set()
        if hasattr(self, 'children'):
            mini_tasks = self.children.all()
            for t in mini_tasks:
                if hasattr(t, 'reports'):
                    l.add(t.reports.all())
                l.add(t.get_all_reports())
            return l
        else:
            return None


class TaskType(models.Model):
    type = models.CharField(max_length=10)

    def __str__(self):
        return self.type


class Report(models.Model):
    owner = models.ForeignKey('Task', related_name='reports', verbose_name='Задание')
    done_count = models.IntegerField(default=0, verbose_name='Сделано')
    name = models.CharField(max_length=15, verbose_name='Название')
    description = models.TextField(verbose_name='Отчёт')

    def __str__(self):
        return self.name


class File(models.Model):
    owner = models.ForeignKey('Report', related_name='files', verbose_name='Отчёт')
    file = models.FileField(verbose_name='Файл')
