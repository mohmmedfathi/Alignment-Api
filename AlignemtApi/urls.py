"""AlignemtApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from Global.views import Global_Get_Post
from local.views import Local_Get_Post
from functions.views import SwissProt_Get_Post
from rest_framework import permissions


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/alignment/global/', Global_Get_Post),
    path('api/alignment/local/', Local_Get_Post),
    path('api/database/swissprot/', SwissProt_Get_Post),

]
