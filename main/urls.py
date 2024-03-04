"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from webbot.views import Adresses, address_select_view, RegionListView, GetChildrenLocations, get_children_locations, bx, Zayavka, RegisterView , LoginView , Bx_router , UploadPassportView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', address_select_view, name='select-address'),
    path('addresses/', Adresses.as_view()),
    path('get-children-locations/', get_children_locations, name='get-children-locations'),
    path('region_list/', RegionListView.as_view(), name='region-list'),
    path('get_child/', GetChildrenLocations.as_view()),
    path('bx/', bx.as_view()),
    path('zayavka/', Zayavka.as_view()),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('send-data-router/', Bx_router.as_view(), name='send-data-router'),
    path('upload-passport/', UploadPassportView.as_view(), name='upload-passport'),
]

