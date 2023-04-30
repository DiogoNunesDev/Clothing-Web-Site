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
    path('addProduct_view/', views.addProduct, name='addProduct'),
    path('add_Product/', views.redirectAddProduct, name='redirectAddProduct'),
    path('tshirts/', views.tshirts_view, name='tshirt'),
    path('<int:produto_id>/detail/', views.detail_view, name='detail'),
    path('edit_Profile/', views.redirectEditProfile, name="redirectEditProfile"),
    path('editProfile_view/', views.edit_profile, name="edit_profile"),
    path('redirectDeleteStaff/', views.redirectDeleteStaff, name='redirectDeleteStaff'),
    path('delete_staff/<int:staff_id>/', views.delete_staff, name='delete_staff'),
    path('comentarios', views.comentarios, name='comentarios'),

]
