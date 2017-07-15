from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^profile/(?P<user_id>[0-9]+)$', views.profile, name='profile'),
    #  редирект сюда после авторизации
    url(r'^stats/(?P<user_id>[0-9]+)$', views.stats, name='stats'),
    url(r'^stats/employee/$', views.employees, name='employees'),
    url(r'^tasks/employees/', views.employees_tasks, name='employees_tasks'),
    url(r'^tasks/$', views.tasks, name='tasks'),
    url(r'^stats/reports/(?P<task_id>[0-9]+)$', views.report_list, name='report_list'),
    url(r'^stats/report/(?P<report_id>[0-9]+)$', views.report, name='report'),
    url(r'^$', views.redirect_to_login_page, name='redirect_to_login_page'),
]