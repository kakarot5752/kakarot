from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^loginHandle/', views.loginHandle),
    url(r'^sendmsg/', views.sendmsg),
    url(r'^check_uname/', views.check_uname),
    url(r'^registerHandle/', views.registerHandle),
    url(r'^check_umsg/', views.check_umsg)
]