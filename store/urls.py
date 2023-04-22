from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("full_collection/", views.full_collection, name="full_collection"),
    path('login/', views.redirectLogin, name='redirectLogin'),
    path('login_view/', views.login_view, name='login_view'),
    path('signup/', views.redirectSignup, name='redirectSignup'),
    path('signup_view/', views.signup_view, name='signup_view'),
    path('carrinho/', views.cart_view, name='cart_view'),


]
