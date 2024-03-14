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
from webbot.views import Adresses, RegionListView, GetChildrenLocations, get_children_locations, \
    bx, CreateZayavka, RegisterView, LoginView, LogoutView, Bx_router, UploadPassportView, \
    CreateSupervizor, CreateAgent, MyZayavki

from webbot.views.neactivka import Bx_neaktivka , Neaktivka_Region

urlpatterns = [
    path('admin/', admin.site.urls),
    path('addresses/', Adresses.as_view()),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('super/', CreateSupervizor.as_view(), name='supervizer'),
    path('agent/', CreateAgent.as_view(), name='agent'),

    path('get-children-locations/', get_children_locations, name='get-children-locations'),
    path('region_list/', RegionListView.as_view(), name='region-list'),
    path('get_child/', GetChildrenLocations.as_view()),
    path('bx/', bx.as_view()),

    path('z/', CreateZayavka.as_view()),
    path('mazay/', MyZayavki.as_view()),
    path('send-data-router/', Bx_router.as_view(), name='send-data-router'),
    path('upload-passport/', UploadPassportView.as_view(), name='upload-passport'),

    path('neactivka/' ,Bx_neaktivka.as_view(),name ='neactivka-reg'),
    path('neactivka_regions/',Neaktivka_Region.as_view(), name = 'neactivka-regions')
    
]
