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
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from pictures.conf import get_settings
from rest_framework.authtoken.views import obtain_auth_token

from music.urls import api_router_v1 as music_api_router_v1
from music_muse.views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/v1/", include(music_api_router_v1.urls)),
    path("", include("django_prometheus.urls")),
    path("api/auth/", obtain_auth_token, name="api_token_auth"),
    path("api/auth/", include("rest_framework.urls")),
]

if get_settings().USE_PLACEHOLDERS:
    urlpatterns.append(
        path("_pictures/", include("pictures.urls")),
    )
