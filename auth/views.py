from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from KPITest import views


def log_in(request):
    if request.method == 'GET':

        return render(request, 'auth/auth.html', {})

    else:
        password = request.POST['password']
        username = request.POST['username']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                return redirect(reverse(views.profile, args={user.id}))
            else:
                # куда?

                return redirect(request.path)

        return redirect(request.path)


