from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.decorators.cache import never_cache
from django.contrib.sessions.models import Session
# from django.contrib.auth.models import User

# Create your views here.
# @user_passes_test(lambda u: not u.is_authenticated, login_url=reverse_lazy('dashboard'))
def login(request):
    if request.method == 'POST':
        # LOGIN
        username = request.POST['username']
        password  =request.POST['password']
        # if Session.objects.filter(usersession__user__username=username).exists():
        #   messages.error(request, 'You are already logged in')
        #   return redirect('gms_login')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            print('login failed')
            messages.error(request, 'Invalid credentials')
            return redirect('gms_login')
        return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('login')

