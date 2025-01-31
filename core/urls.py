"""
URL configuration for music_muse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.contrib import admin
from django.urls import include, path
from pictures.conf import get_settings

from core.api import api
from core.settings import HEALTH_SECRET_TOKEN
from core.views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index),
    path("api/", api.urls),
    path(rf'ht/{HEALTH_SECRET_TOKEN}/', include('health_check.urls')),
]

if get_settings().USE_PLACEHOLDERS:
    urlpatterns.append(
        path("_pictures/", include("pictures.urls")),
    )
