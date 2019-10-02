from django.contrib import admin
from MenuServe.models import Menu,Store,Manager,Employee,MenuOrder,Order,Cart

 
# Register your models here.
admin.site.register(Menu)
admin.site.register(Store)
admin.site.register(Manager)
admin.site.register(Employee)
admin.site.register(Order)
admin.site.register(MenuOrder)
admin.site.register(Cart)

