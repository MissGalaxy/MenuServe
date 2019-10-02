from django.db import models

# Create your models here.

class Menu(models.Model):
	name=models.CharField(max_length=100)
	price=models.FloatField()
	description=models.TextField()
	photo=models.ImageField()

	class Meta:
		verbose_name=("Menu")
		verbose_name_plural=("Menus")

class Manager(models.Model):
	name=models.CharField(max_length=100)

class Employee(models.Model):
	name=models.CharField(max_length=100)
	manager=models.ForeignKey(Manager, on_delete=models.CASCADE,default='')

class Store(models.Model):
	name=models.CharField(max_length=100)
	address=models.CharField(max_length=500)
	manager=models.ManyToManyField(Manager)
	employee=models.ManyToManyField(Employee)

class Order(models.Model):
	address=models.CharField(max_length=500)
	store=models.CharField(max_length=100)
	price=models.FloatField()
	menus=models.ManyToManyField(Menu,through='MenuOrder')
	status=models.BooleanField(blank=False)

class MenuOrder(models.Model):
	order = models.ForeignKey(Order,on_delete=models.CASCADE)
	menu = models.ForeignKey(Menu,on_delete=models.CASCADE)
	num = models.IntegerField()

class Cart(models.Model):
	menuId=models.IntegerField()
	name=models.CharField(max_length=100)
	price=models.FloatField()
	description=models.TextField()
	photo=models.ImageField()
	num=models.IntegerField()
		


		
			


