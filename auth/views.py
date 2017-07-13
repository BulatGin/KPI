from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
from django.urls import reverse

from KPITest import views
from KPITest.models import Employee


def log_in(request):
    if request.method == 'GET':
        # template =
        # заменить
        return render(request, 'auth/login_form.html', {})
    else:
        password = request.POST['password']
        username = request.POST['username']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse(views.stats, args={user.id}))
            else:
                # куда?
                return redirect(request.path)

        return redirect(request.path)
