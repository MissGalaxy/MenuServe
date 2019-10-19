from django.db import models

class Menu(models.Model):
	name=models.CharField(max_length=100)
	price=models.FloatField()
	description=models.TextField()
	photo=models.ImageField()

	class Meta:
		verbose_name=("Menu")
		verbose_name_plural=("Menus")

class Customer(models.Model):
	username=models.CharField(max_length=100, primary_key=True)

class Manager(models.Model):
	username=models.CharField(max_length=100, primary_key=True)

class Employee(models.Model):
	username=models.CharField(max_length=100, primary_key=True)

class Store(models.Model):
	name=models.CharField(max_length=100)
	address=models.CharField(max_length=500)
	staff=models.CharField(max_length=1000)

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
		
