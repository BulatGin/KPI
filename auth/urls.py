from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.log_in, name='auth'),
]
