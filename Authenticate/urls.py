from os import name
from django.urls.resolvers import URLPattern
from django.urls import path
from Authenticate import views

urlpatterns=[
    path("",views.index,name="index"),
    path("login",views.index,name="index"),
    path("sign_up",views.signup,name="register"),
    path("sign_up_added",views.sigupadded,name="register sub"),
    path("add_user",views.add_user,name="adduser"),
    path("device_operations",views.device_operations,name="deviceoperation"),
    path("home",views.home,name="home"),
    path("add_device",views.device_operations,name='add_device'),
    path("logout",views.logout,name='logout'),
    path("schedule",views.schedule, name="schedule"),
    path("edit_user_details",views.edit_user_details, name="edit_user_details"),
    path("edit_devices_details",views.edit_devices_details, name="edit_devices_details"),

]
