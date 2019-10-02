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
    path('order/',views.order,name='order'),
	path('admin/', admin.site.urls)
]