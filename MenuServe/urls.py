from . import views
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
	path('', views.menu,name='menu'),
    path('manage_menu/',views.manage_menu,name='manage_menu'),
    path('manage_store/',views.manage_store,name='manage_store'),
    path('manage_manager/',views.manage_manager,name='manage_manager'),
    path('manage_employee/',views.manage_employee,name='manage_employee'),
    path('manage_order/',views.manage_order,name='manage_order'),
    path('manage_role/',views.manage_role,name='manage_role'),
    path('order/',views.order,name='order'),
	path('signin/',views.signin,name='signin'),
	path('login/',views.loginView,name='login'),
	path('logout/',views.logoutView,name='logout'),
    path('add_to_cart/',views.add_to_cart,name='add_to_cart'),
    path('change_cart_item/',views.change_cart_item,name='change_cart_item'),
    path('refresh_order/',views.refresh_order,name='refresh_order'),
	path('admin/', admin.site.urls)
]