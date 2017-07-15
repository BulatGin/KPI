from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden


def is_director(funct=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=HttpResponseForbidden):
    decorator = user_passes_test(
        lambda u: u.employee.is_director(),
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if funct:
        return decorator(funct)
    else:
        return decorator

