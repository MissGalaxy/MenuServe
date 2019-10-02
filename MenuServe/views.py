from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import Menu,Manager,Employee,Store,Order,MenuOrder,Cart

def menu(request):
	menus = Menu.objects.all()
	addRes=""
	if 'addToCart' in request.POST:
		menuId=request.POST.get('addToCart')
		result= Cart.objects.filter(menuId=menuId)
		if result.count() == 0:
			try:
				menu=Menu.objects.get(id=menuId)
			except Menu.DoesNotExist:
				addRes="menu Id doesn't exist"
			else:
				dish=Cart(menuId=menu.id,name=menu.name,price=menu.price,description=menu.description, photo=menu.photo, num=1)
				dish.save()	
	return render(request,'menu.html',{"menus":menus})
def order(request):
	items= Cart.objects.all()
	stores= Store.objects.all()
	removeRes=""
	plusRes=""
	minusRes=""
	totalPrice=0
	for item in items:
		totalPrice+=item.num*item.price
	if 'removeFromCart' in request.POST:
		itemId=request.POST.get('removeFromCart')
		try:
			item=Cart.objects.get(id=itemId)
		except Cart.DoesNotExist:
			removeRes="item id doesn't exist"
		else:
			item.delete()
	if 'itemMinus' in request.POST:
		itemId=request.POST.get('itemMinus')
		try:
			item=Cart.objects.get(id=itemId)
		except Cart.DoesNotExist:
			minusRes="item id doesn't exist"
		else:
			t=item.num
			if t>1:
				item.num=t-1
				item.save()
	if 'itemPlus' in request.POST:
		itemId=request.POST.get('itemPlus')
		try:
			item=Cart.objects.get(id=itemId)
		except Cart.DoesNotExist:
			plusRes="item id doesn't exist"
		else:
			t=item.num
			item.num=t+1
			item.save()
	if 'placeOrder' in request.POST:
		address=request.POST.get('orderAddress')
		store=request.POST.get('chooseStore')
		order=Order.objects.create(address=address,store=store,price=totalPrice,status=False)
		for item in items:
			menu=Menu.objects.get(id=item.menuId)
			menuorder=MenuOrder(order=order,menu=menu,num=item.num)
			menuorder.save()
		order.save()
		Cart.objects.all().delete()
	return render(request,'order.html',{"items":items,"totalPrice":totalPrice,"stores":stores})
def manage_menu(request):
	menus = Menu.objects.all()
	deleteRes=''
	editRes=''
	if 'deleteId' in request.POST:
		id=request.POST.get('deleteId')
		if str.isdigit(id):
			try :
				dish = Menu.objects.get(id=id)
			except Menu.DoesNotExist:
				deleteRes='Dish Id does not exist'
			else:
				dish.delete()
				deleteRes='Delete succeed'
	if 'addName' in request.POST and 'addPrice' in request.POST and 'addDes' in request.POST:
		myfile = request.FILES.get('addPhoto')
		fs=FileSystemStorage()
		if myfile:
			file=fs.save(myfile.name,myfile)
			name=request.POST.get('addName')
			price=request.POST.get('addPrice')
			description=request.POST.get('addDes')
			photo=file
			dish=Menu(name=name,price=price,description=description,photo=photo)
			dish.save()
	if 'editId' in request.POST and 'editName' in request.POST and 'editPrice' in request.POST and 'editDes' in request.POST:
		myfile = request.FILES.get('editPhoto')
		fs=FileSystemStorage()
		if myfile:
			file=fs.save(myfile.name,myfile)
			editId=request.POST.get('editId')
			name=request.POST.get('editName')
			price=request.POST.get('editPrice')
			description=request.POST.get('editDes')
			photo=file
			try:
				dish=Menu.objects.get(id=editId)
			except Memu.DoesNotExist:
				editRes='edit id does not exist'
			else:
				dish.name=name
				dish.price=price
				dish.description=description
				dish.photo=photo
				dish.save()
	return render(request,'manage_menu.html',{"menus":menus})

def manage_store(request):
	stores=Store.objects.all()
	addRes=''
	deleteRes=''
	editRes=''
	if 'deleteId' in request.POST:
		id=request.POST.get('deleteId')
		if str.isdigit(id):
			try :
				store =Store.objects.get(id=id)
			except Store.DoesNotExist:
				deleteRes='Delete Id does not exist'
			else:
				store.delete()
	if 'addName' in request.POST and 'addAddress' in request.POST and 'addManager' in request.POST and 'addEmployee' in request.POST:
		name=request.POST.get('addName')
		address=request.POST.get('addAddress')
		tmanagers=request.POST.get('addManager')
		temployees=request.POST.get('addEmployee')
		managers=tmanagers.split(',')
		employees=temployees.split(',')
		store=Store.objects.create(name=name,address=address)
		for manager in managers:
			store.manager.add(manager)
		for employee in employees:
			store.employee.add(employee)
		store.save()
	if 'editName' in request.POST and 'editAddress' in request.POST and 'editManager' in request.POST and 'editEmployee' in request.POST:
		editId=request.POST.get('editId')
		name=request.POST.get('editName')
		address=request.POST.get('editAddress')
		tmanagers=request.POST.get('editManager')
		temployees=request.POST.get('editEmployee')
		managers=tmanagers.split(',')
		employees=temployees.split(',')
		try:
			store=Store.objects.get(id=editId)
		except Store.DoesNotExist:
			editRes='edit Id does not exist'
		else:
			store.name=name
			store.address=address
			store.manager.clear()
			store.employee.clear()
			for manager in managers:
				store.manager.add(manager)
			for employee in employees:
				store.employee.add(employee)
			store.save()
	return render(request,'manage_store.html',{"stores":stores})
def manage_manager(request):
	managers = Manager.objects.all()
	deleteRes=''
	editRes=''
	if 'deleteId' in request.POST:
		id=request.POST.get('deleteId')
		if str.isdigit(id):
			try :
				manager = Manager.objects.get(id=id)
			except Manager.DoesNotExist:
				deleteRes='Delete Id does not exist'
			else:
				manager.delete()
	if 'addName' in request.POST:
		name=request.POST.get('addName')
		manager=Manager(name=name)
		manager.save()
	if 'editId' in request.POST and 'editName' in request.POST:
		editId=request.POST.get('editId')
		name=request.POST.get('editName')
		try:
			manager=Manager.objects.get(id=editId)
		except Manager.DoesNotExist:
			editRes='edit Id does not exist'
		else:
			manager.name=name
			manager.save()
	return render(request,'manage_manager.html',{"managers":managers})
def manage_employee(request):
	employees = Employee.objects.all()
	deleteRes=''
	editRes=''
	addRes=''
	if 'deleteId' in request.POST:
		id=request.POST.get('deleteId')
		if str.isdigit(id):
			try :
				employee = Employee.objects.get(id=id)
			except Employee.DoesNotExist:
				deleteRes='Delete Id does not exist'
			else:
				employee.delete()
	if 'addName' in request.POST:
		name=request.POST.get('addName')
		managerId=request.POST.get('addManagerId')
		if str.isdigit(managerId):
			try :
				manager=Manager.objects.get(id=managerId)
			except Manager.DoesNotExist:
				addRes='Manager Id does not exist'
			else:
				employee=Employee(name=name,manager=manager)
				employee.save()
	if 'editId' in request.POST and 'editName' in request.POST:
		editId=request.POST.get('editId')
		name=request.POST.get('editName')
		managerId=request.POST.get('editManagerId')
		if str.isdigit(managerId):
			try :
				manager=Manager.objects.get(id=managerId)
			except Manager.DoesNotExist:
				editRes='Manager Id does not exist'
			else:
				if str.isdigit(editId):
					try:
						employee=Employee.objects.get(id=editId)
					except Employee.DoesNotExist:
						editRes='edit employee Id does not exist'
					else:
						employee.name=name
						employee.manager=manager
						employee.save()
	return render(request,'manage_employee.html',{"employees":employees})
def manage_order(request):
	orders = Order.objects.all()
	if request.method == "POST":
		orderId=request.POST.get('fulfill')
		order=Order.objects.get(id=orderId)
		order.status=True
		order.save()
	return render(request,'manage_order.html',{"orders":orders})
	
