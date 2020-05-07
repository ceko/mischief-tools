"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from .api import views as api_views
from rest_framework import routers
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views
from importlib import import_module

from allauth.socialaccount import providers
from allauth.account import views as allauth_views
from django.conf import settings

provider_urlpatterns = []
for provider in providers.registry.get_list():
    try:
        prov_mod = import_module(provider.get_package() + '.urls')
    except ImportError:
        continue
    prov_urlpatterns = getattr(prov_mod, 'urlpatterns', None)
    if prov_urlpatterns:
        provider_urlpatterns += prov_urlpatterns

urlpatterns = [
    path('', views.index),
    path('logout/', views.logout),

    path('admin/', admin.site.urls),
    url(r'^accounts/', include(
        provider_urlpatterns + [
            path('login/', allauth_views.login, name="account_login"),
            path("signup/", allauth_views.signup, name="account_signup"),
        ]
    )),
    path('social/', include('allauth.socialaccount.urls'))
]


router = routers.DefaultRouter()

router.register('priorities', api_views.PriorityViewSet)
router.register('items', api_views.ItemViewSet)
urlpatterns += [path('api/v1/', include(router.urls)), ]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
