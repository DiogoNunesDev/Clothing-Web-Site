from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("index/", views.index, name="index"),
    path('redirectLogin/', views.redirectLogin, name='redirectLogin'),
    path('login_view/', views.login_view, name='login_view'),
    path('redirectSignup/', views.redirectSignup, name= 'redirectSignup'),
    path('signup_view/', views.signup_view, name='signup_view'),

]
