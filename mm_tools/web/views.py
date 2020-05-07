from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as logout_user


@login_required
def index(request):
    return render(request, 'mm_tools.web/client.html')


def logout(request):
    logout_user(request)
    return redirect('/')
