"""tvshow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path

from django.conf.urls import include

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views as auth_views

from tvshowapp import views
from frontend import urls as frontend_urls

urlpatterns = [
    path('', include(frontend_urls)),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/candidates/', views.CandidateList.as_view()),
    path('api/candidates/<int:pk>/', views.CandidateDetail.as_view()),
    path('api/teams/', views.TeamList.as_view()),
    path('api/teams/<int:pk>/', views.TeamDetail.as_view()),
    path('api/login/', views.login),
]

urlpatterns = format_suffix_patterns(urlpatterns)