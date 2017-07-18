from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden, HttpResponse


def is_director(function):
  def wrap(request, *args, **kwargs):
        if request.user.employee.is_director():
             return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
  return wrap


def can_watch_page(function):
  def wrap(request, *args, **kwargs):
        if request.user.employee.can_watch_page(request.user.employee):
             return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
  return wrap

