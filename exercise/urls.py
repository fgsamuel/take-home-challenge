"""exercise URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter

from xml_converter import views, api

router = DefaultRouter()
router.register('converter', api.ConverterViewSet, basename='converter')

urlpatterns = [
    path('', RedirectView.as_view(url='connected/')),
    path('admin/', admin.site.urls),
    path('connected/', views.upload_page, name='upload_page'),
    path('api/', include(router.urls)),
]
