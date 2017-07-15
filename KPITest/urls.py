from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^profile/(?P<user_id>[0-9]+)$', views.profile, name='profile'),
    #  редирект сюда после авторизации
    url(r'^stats/(?P<user_id>[0-9]+)$', views.stats, name='stats'),
    url(r'^logout/',views.log_out, name='logout'),
    url(r'^stats/employees/$', views.employees, name='employees'),
    url(r'^stats/report/(?P<report_id>[0-9]+)$', views.report, name='report'),
    url(r'^stats/reports/(?P<task_id>[0-9]+)$', views.reports_list, name='reports_list'),
    url(r'^tasks/(?P<user_id>[0-9]+)$', views.tasks, name='tasks'),
    url(r'^tasks/update/(?P<task_id>[0-9]+)$', views.update_task, name='update_task'),
    url(r'^tasks/create$', views.create_task, name='create_task'),
    url(r'^tasks/execute/(?P<task_id>[0-9]+)$', views.execute_task, name='execute_task'),
    url(r'^tasks/employees/$', views.employees_tasks, name='employees_tasks'),
    url(r'^$', views.redirect_to_login_page, name='redirect_to_login_page'),
]