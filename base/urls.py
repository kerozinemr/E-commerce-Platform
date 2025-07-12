from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register, name='register'),
    path('accounts/login/',views.loginPage, name='login'),
    path('logout/',views.logoutUser, name='logout'),
    path('',views.store,name='store'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('profile/',views.profile, name='profile'),
    path('update_item/', views.updateItem, name="update_itme"),
    path('process_order/', views.processOrder, name='processo_rder'),
    ]
