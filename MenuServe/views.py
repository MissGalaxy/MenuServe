from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.core.files.storage import FileSystemStorage
from .models import Menu,Customer,Manager,Employee,Store,Order,MenuOrder,Cart
from .forms import *
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User,Group,Permission,ContentType

customerG,flag1=Group.objects.get_or_create(name='Customer')
employeeG,flag2=Group.objects.get_or_create(name='Employee')
managerG,flag3=Group.objects.get_or_create(name='Manager')

content_type = ContentType.objects.get_for_model(Store)
permission = Permission.objects.filter(content_type=content_type)
managerG.permissions.set(permission)
content_type2 = ContentType.objects.get_for_model(User)
permission2 = Permission.objects.filter(content_type=content_type2)
managerG.permissions.set(permission2)
content_type3 = ContentType.objects.get_for_model(Menu)
permission3 = Permission.objects.filter(content_type=content_type3)
managerG.permissions.set(permission3)
content_type4 = ContentType.objects.get_for_model(Order)
permission4 = Permission.objects.filter(content_type=content_type4)
managerG.permissions.set(permission4)
employeeG.permissions.set(permission4)

def signin(request):
	result=""
	signinForm=SignInForm()
	if request.method == "POST":
		signinForm=SignInForm(request.POST)
		if signinForm.is_valid():
			username = signinForm.cleaned_data.get("username")
			password = signinForm.cleaned_data.get("password1")
			firstName = signinForm.cleaned_data.get("firstname")
			lastName = signinForm.cleaned_data.get("lastname")
			username_exists = User.objects.filter(username=username).exists()
			if not username_exists:
				user=User.objects.create_user(username=username,password=password,first_name=firstName,last_name=lastName)
				# customer=Customer(username=username)
				# customer.save()
				group=Group.objects.get(name='Customer')
				user.groups.add(group)
				result="regist succeed!"
				return redirect('menu')
			else:
				result="username exist!"
	return render(request,'signin.html',{"result":result,"form":signinForm})

def loginView(request):
	result=""
	loginForm=LogInForm()
	if request.method == "POST":
		loginForm=LogInForm(request.POST)
		if loginForm.is_valid():
			username = loginForm.cleaned_data.get("username")
			password = loginForm.cleaned_data.get("password")
			user = authenticate(request,username=username,password=password)
			if user and user.is_active:
				login(request,user)
				result="log in succeed"
				request.session.set_expiry(0)
				return redirect('menu')

			elif user and not user.is_active:
				result="user is not active"
			else:
				result="username or password is wrong"
	return render(request,'login.html',{"result":result,"form":loginForm})

def logoutView(request):
    logout(request)
    return redirect('menu')

def menu(request):
	menus = Menu.objects.all()
	# addRes=""
	# if 'addToCart' in request.POST:
	# 	menuId=request.POST.get('addToCart')
	# 	result= Cart.objects.filter(menuId=menuId)
	# 	if result.count() == 0:
	# 		try:
	# 			menu=Menu.objects.get(id=menuId)
	# 		except Menu.DoesNotExist:
	# 			addRes="menu Id doesn't exist"
	# 		else:
	# 			dish=Cart(menuId=menu.id,name=menu.name,price=menu.price,description=menu.description, photo=menu.photo, num=1)
	# 			dish.save()	
	return render(request,'menu.html',{"menus":menus})

@login_required(login_url='login')
def order(request):
	items= Cart.objects.all()
	stores= Store.objects.all()
	removeRes=""
	plusRes=""
	minusRes=""
	totalPrice=0
	for item in items:
		totalPrice+=item.num*item.price

	orders={}
	username=request.user.username
	username_exists=User.objects.filter(username=username)
	if username_exists:
		orders=Order.objects.filter(customer=username)

	# if 'removeFromCart' in request.POST:
	# 	itemId=request.POST.get('removeFromCart')
	# 	try:
	# 		item=Cart.objects.get(id=itemId)
	# 	except Cart.DoesNotExist:
	# 		removeRes="item id doesn't exist"
	# 	else:
	# 		item.delete()
	# if 'itemMinus' in request.POST:
	# 	itemId=request.POST.get('itemMinus')
	# 	try:
	# 		item=Cart.objects.get(id=itemId)
	# 	except Cart.DoesNotExist:
	# 		minusRes="item id doesn't exist"
	# 	else:
	# 		t=item.num
	# 		if t>1:
	# 			item.num=t-1
	# 			item.save()
	# if 'itemPlus' in request.POST:
	# 	itemId=request.POST.get('itemPlus')
	# 	try:
	# 		item=Cart.objects.get(id=itemId)
	# 	except Cart.DoesNotExist:
	# 		plusRes="item id doesn't exist"
	# 	else:
	# 		t=item.num
	# 		item.num=t+1
	# 		item.save()
	if 'placeOrder' in request.POST and username:
		address=request.POST.get('orderAddress')
		store=request.POST.get('chooseStore')
		order=Order.objects.create(address=address,store=store,price=totalPrice,status=False,customer=username)
		description=""
		for item in items:
			menu=Menu.objects.get(id=item.menuId)
			menuorder=MenuOrder(order=order,menu=menu,num=item.num)
			menuorder.save()
			description+=str(item.name)+" "+str(item.num)+" "
		order.description=description
		order.save()
		Cart.objects.all().delete()
		items= Cart.objects.all()
		totalPrice=0
	return render(request,'order.html',{"items":items,"totalPrice":totalPrice,"stores":stores,"orders":orders})

# @permission_required('Menu.view_menu')
def manage_menu(request):
	currgroup=request.user.groups.all()
	if not str(currgroup[0]) == "Manager":
		return redirect('menu')

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
		else:
			name=request.POST.get('addName')
			price=request.POST.get('addPrice')
			description=request.POST.get('addDes')
			dish=Menu(name=name,price=price,description=description)
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

# def manage_store(request):
# 	stores=Store.objects.all()
# 	addRes=''
# 	deleteRes=''
# 	editRes=''
# 	if 'deleteId' in request.POST:
# 		id=request.POST.get('deleteId')
# 		if str.isdigit(id):
# 			try :
# 				store =Store.objects.get(id=id)
# 			except Store.DoesNotExist:
# 				deleteRes='Delete Id does not exist'
# 			else:
# 				store.delete()
# 	if 'addName' in request.POST and 'addAddress' in request.POST and 'addManager' in request.POST and 'addEmployee' in request.POST:
# 		name=request.POST.get('addName')
# 		address=request.POST.get('addAddress')
# 		tmanagers=request.POST.get('addManager')
# 		temployees=request.POST.get('addEmployee')
# 		managers=tmanagers.split(',')
# 		employees=temployees.split(',')
# 		store=Store.objects.create(name=name,address=address)
# 		for manager in managers:
# 			store.manager.add(manager)
# 		for employee in employees:
# 			store.employee.add(employee)
# 		store.save()
# 	if 'editName' in request.POST and 'editAddress' in request.POST and 'editManager' in request.POST and 'editEmployee' in request.POST:
# 		editId=request.POST.get('editId')
# 		name=request.POST.get('editName')
# 		address=request.POST.get('editAddress')
# 		tmanagers=request.POST.get('editManager')
# 		temployees=request.POST.get('editEmployee')
# 		managers=tmanagers.split(',')
# 		employees=temployees.split(',')
# 		try:
# 			store=Store.objects.get(id=editId)
# 		except Store.DoesNotExist:
# 			editRes='edit Id does not exist'
# 		else:
# 			store.name=name
# 			store.address=address
# 			store.manager.clear()
# 			store.employee.clear()
# 			for manager in managers:
# 				store.manager.add(manager)
# 			for employee in employees:
# 				store.employee.add(employee)
# 			store.save()
# 	return render(request,'manage_store.html',{"stores":stores})
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

# @permission_required('Order.view_order')
def manage_order(request):
	currgroup=request.user.groups.all()
	if not (str(currgroup[0]) == "Manager" or str(currgroup[0]) == "Employee"):
		return redirect('menu')

	orders = Order.objects.all()
	if request.method == "POST":
		orderId=request.POST.get('fulfill')
		order=Order.objects.get(id=orderId)
		order.status=True
		order.save()
	return render(request,'manage_order.html',{"orders":orders})

# @permission_required('Store.view_store')
def manage_store(request):
	currgroup=request.user.groups.all()
	if not str(currgroup[0]) == "Manager":
		return redirect('menu')
	stores=Store.objects.all()
	if 'deleteId' in request.POST:
		storeId=request.POST.get('deleteId')
		if str.isdigit(storeId):
			store =Store.objects.get(id=storeId)
			if store:
				store.delete()
	if 'addName' in request.POST and 'addAddress' in request.POST:
		name=request.POST.get('addName')
		address=request.POST.get('addAddress')
		store=Store.objects.create(name=name,address=address)
		store.save()
	if 'UserName' in request.POST and 'AssginID' in request.POST :
		username=request.POST.get('UserName')
		storeId=request.POST.get('AssginID')
		username_exists = User.objects.filter(username=username).exists()
		store=Store.objects.get(id=storeId)
		if username_exists and store:
			store.staff=store.staff+","+username
			store.save()

	return render(request,'manage_store.html',{"stores":stores})

# def manage_role(request):
# 	customers=Customer.objects.all()
# 	managers=Manager.objects.all()
# 	employees=Employee.objects.all()
# 	addManagerRes=""
# 	deleteManagerRes=""
# 	addEmployeeRes=""
# 	deleteEmployeeRes=""
# 	if 'addManager' in request.POST:
# 		username=request.POST.get('addManager')
# 		username_exists = User.objects.filter(username=username).exists()
# 		if username_exists:
# 			manager_exists = Manager.objects.filter(username=username).exists()
# 			if not manager_exists:
# 				manager=Manager(username=username)
# 				manager.save()
# 			customer_exists = Customer.objects.filter(username=username).exists()
# 			if customer_exists:
# 				customer=Customer.objects.filter(username=username)
# 				customer.delete()
# 			employee_exists = Employee.objects.filter(username=username).exists()
# 			if employee_exists:
# 				employee=Employee.objects.filter(username=username)
# 				employee.delete()
# 			addManagerRes="Add Manager Succeed!"
# 		else:
# 			addManagerRes="Add Manager Failed! User doesn't exist"
# 	if 'deleteManager' in request.POST:
# 		username=request.POST.get('deleteManager')
# 		username_exists = User.objects.filter(username=username).exists()
# 		if username_exists:
# 			manager_exists = Manager.objects.filter(username=username).exists()
# 			if manager_exists:
# 				manager = Manager.objects.filter(username=username)
# 				manager.delete()
# 			customer_exists=Customer.objects.filter(username=username)
# 			if not customer_exists:
# 				customer=Customer(username=username)
# 				customer.save()
# 			deleteManagerRes="Delete Manager succeed!"
# 		else:
# 			deleteManagerRes="Delete Manager Failed! User doesn't exist"
# 	if 'addEmployee' in request.POST:
# 		username=request.POST.get('addEmployee')
# 		username_exists = User.objects.filter(username=username).exists()
# 		if username_exists:
# 			employee_exists = Employee.objects.filter(username=username).exists()
# 			if not employee_exists:
# 				employee=Employee(username=username)
# 				employee.save()
# 			customer_exists = Customer.objects.filter(username=username).exists()
# 			if customer_exists:
# 				customer=Customer.objects.filter(username=username)
# 				customer.delete()
# 			manager_exists = Manager.objects.filter(username=username).exists()
# 			if manager_exists:
# 				manager=Manager.objects.filter(username=username)
# 				manager.delete()
# 			addEmployeeRes="Add Employee Succeed!"
# 		else:
# 			addEmployeeRes="Add Employee Failed! User doesn't exist"
# 	if 'deleteEmployee' in request.POST:
# 		username=request.POST.get('deleteEmployee')
# 		username_exists = User.objects.filter(username=username).exists()
# 		if username_exists:
# 			employee_exists = Employee.objects.filter(username=username).exists()
# 			if employee_exists:
# 				employee = Employee.objects.filter(username=username)
# 				employee.delete()
# 			customer_exists=Customer.objects.filter(username=username)
# 			if not customer_exists:
# 				customer=Customer(username=username)
# 				customer.save()
# 			deleteEmployeeRes="Delete Employee succeed!"
# 		else:
# 			deleteEmployeeRes="Delete Employee Failed! User doesn't exist"
	
# 	return render(request,'manage_role.html',{"customers":customers,"managers":managers,"employees":employees,'addManagerRes':addManagerRes,'deleteManagerRes':deleteManagerRes})

# @permission_required('User.view_user',login_url='login')
def manage_role(request):
	currgroup=request.user.groups.all()
	if not str(currgroup[0]) == "Manager":
		return redirect('menu')

	users=User.objects.all()
	groups=Group.objects.all()
	if 'username' in request.POST and 'groupSelect' in request.POST:
		username=request.POST.get('username')
		groupName=request.POST.get('groupSelect')
		username_exists = User.objects.filter(username=username).exists()
		group=Group.objects.get(name=groupName)
		if username_exists and group:
			user=User.objects.get(username=username)
			user.groups.clear()
			user.groups.add(group)
			user.save()
	return render(request,'manage_role.html',{"users":users,"groups":groups})

def add_to_cart(request):
	addRes=""
	if 'menu_id' in request.GET:
		menuId=request.GET.get('menu_id')
		result= Cart.objects.filter(menuId=menuId)
		if result.count() == 0:
			try:
				menu=Menu.objects.get(id=menuId)
			except Menu.DoesNotExist:
				addRes="menu Id doesn't exist"
			else:
				dish=Cart(menuId=menu.id,name=menu.name,price=menu.price,description=menu.description, photo=menu.photo, num=1)
				dish.save()	
	return HttpResponse()

def change_cart_item(request):
	removeRes=""
	minusRes=""
	minusRes=""
	data={}
	print("test cart item")
	if 'remove_item_id' in request.GET:
		itemId=request.GET.get('remove_item_id')
		print("item is is:"+itemId)
		try:
			item=Cart.objects.get(id=itemId)
		except Cart.DoesNotExist:
			removeRes="item id doesn't exist"
		else:
			item.delete()
			data['item_id']=itemId
	if 'minus_item_id' in request.GET:
		print("test minus")
		itemId=request.GET.get('minus_item_id')
		try:
			item=Cart.objects.get(id=itemId)
		except Cart.DoesNotExist:
			minusRes="item id doesn't exist"
		else:
			t=item.num
			if t>1:
				t=t-1
				item.num=t
				item.save()
			data['num']=t
			data['item_id']=itemId
	if 'plus_item_id' in request.GET:
		print("test add")
		itemId=request.GET.get('plus_item_id')
		try:
			item=Cart.objects.get(id=itemId)
		except Cart.DoesNotExist:
			plusRes="item id doesn't exist"
		else:
			t=item.num
			t=t+1
			item.num=t
			item.save()
			data['num']=t
			data['item_id']=itemId

	items= Cart.objects.all()
	totalPrice=0
	for item in items:
		totalPrice+=item.num*item.price
	data['totalPrice']=totalPrice
	return JsonResponse(data)

def refresh_order(request):
	data=[]
	orders = Order.objects.all()
	for order in orders:
		temp={}
		temp['id']=order.id
		temp['address']=order.address
		temp['store']=order.store
		temp['price']=order.price
		# temp['menus']=order.menus
		temp['description']=order.description
		temp['status']=order.status
		data.append(temp)
	return JsonResponse(data, safe=False)

