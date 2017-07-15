from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^profile/(?P<user_id>[0-9]+)$', views.profile, name='profile'),
    #  редирект сюда после авторизации
    url(r'^stats/(?P<user_id>[0-9]+)$', views.stats, name='stats'),
    url(r'^logout/',views.log_out, name='logout'),
    url(r'^stats/employee/$', views.employees, name='employees'),
    url(r'^tasks/(?P<user_id>[0-9]+)$', views.tasks, name='tasks'),
    url(r'^tasks/employees/', views.employees_tasks, name='employees_tasks'),
    url(r'^$', views.redirect_to_login_page, name='redirect_to_login_page'),
]