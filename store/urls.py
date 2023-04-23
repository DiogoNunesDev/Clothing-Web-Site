from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("full_collection/", views.full_collection, name="full_collection"),
    path('login/', views.redirectLogin, name='redirectLogin'),
    path('login_view/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('signup/', views.redirectSignup, name='redirectSignup'),
    path('signup_view/', views.signup_view, name='signup_view'),
    path('carrinho/', views.cart_view, name='cart_view'),
    path('addStaff_view/', views.addStaff, name='addStaff'),
    path('addStaff/', views.redirectAddStaff, name='redirectAddStaff'),
    path('sweatshirts/', views.sweatshirts_view, name='sweatshirts'),
    path('profile/', views.profile, name='profile'),
    path('tshirts/', views.tshirts_view, name='tshirt')

]
