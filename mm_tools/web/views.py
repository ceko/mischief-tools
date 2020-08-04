from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as logout_user
import logging

logger = logging.getLogger(__name__)


@login_required
def index(request):
    print(request.user)
    return render(request, 'mm_tools.web/client.html')


def logout(request):
    logout_user(request)
    return redirect('/')
