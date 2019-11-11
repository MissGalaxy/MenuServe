from django.test import TestCase,LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import selenium.webdriver.support.ui as ui
from .models import *
import time 
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import login,logout
from django.contrib.auth.models import User,Group
# Create your tests here.
class TestMenuServe(StaticLiveServerTestCase):
	def setUp(self):
		customerG,flag1=Group.objects.get_or_create(name='Customer')
		employeeG,flag2=Group.objects.get_or_create(name='Employee')
		managerG,flag3=Group.objects.get_or_create(name='Manager')
		self.menu=Menu(name="Dishtest",price="2.2",description="test case",photo="../media/card0.jpg")
		self.menu.save()
		self.test_user1 = User.objects.create_user(username='testuser1', password='12345') 
		self.test_user1.save()
		self.manager = User.objects.create_user(username='manager', password='12345') 
		self.manager.save()
		self.group=Group.objects.get(name='Manager')
		self.manager.groups.add(self.group)
		self.item=Cart.objects.create(menuId="1",name="Dishtest",price="2.2",description="test case",photo="../media/card0.jpg",num="2")
		self.item.save()
		self.store=Store.objects.create(name="storetest",address="streettest")
		self.store.save()
		self.order=Order.objects.create(address="streettest",store="1",price="2.2",status=False)
		self.order.save()

	def test_cart_item_remove(self):
		print("test_cart_item_remove")
		self.driver = webdriver.Chrome()
		self.driver.get(self.live_server_url+"/login/")
	  	#test authentication
		self.driver.find_element_by_id("username").send_keys("testuser1")
		self.driver.find_element_by_id("password").send_keys("12345")
		self.driver.find_element_by_id("login").click()
		self.driver.get(self.live_server_url+"/order/")
		self.driver.find_element_by_id(str(self.item.id)+"removebtn").click()
		time.sleep(1)
		item_exist= Cart.objects.filter(id=str(self.item.id)).exists()
		# print("item exist: "+str(item_exist))
		self.assertFalse(item_exist)

	def test_fulfill_order(self):
		print("test_fulfill_order")
		self.driver = webdriver.Chrome()
		# test authentication of manager
		self.driver.get(self.live_server_url+"/login/")
		self.driver.find_element_by_id("username").send_keys("manager")
		self.driver.find_element_by_id("password").send_keys("12345")
		self.driver.find_element_by_id("login").click()
		self.order1=Order.objects.create(address="streettest1",store="1",price="2.2",status=False)
		self.order1.save()
		self.driver.get(self.live_server_url+"/manage_order/")
		self.driver.find_element_by_id(str(self.order1.id)+"fulfillbtn").click()
		# test model Order
		time.sleep(1)
		self.orderres=Order.objects.get(id=self.order1.id)
		self.assertTrue(self.orderres.status)

	def test_addToCart(self):
		print("test_addToCart")
		# test model Cart
	  	#test authentication
		#login = self.client.login(username='testuser1', password='12345')
		self.driver = webdriver.Chrome()
		self.driver.get(self.live_server_url)
		self.driver.find_element_by_id("1addbtn").click()
		item = Cart.objects.filter(menuId="1")
		self.assertIsNotNone(item)
		# time.sleep(5)

	def  test_cart_place_order(self):
		print("test_cart_place_order")
		self.driver = webdriver.Chrome()
		self.driver.get(self.live_server_url+"/login/")
	  	#test authentication 
		self.driver.find_element_by_id("username").send_keys("testuser1")
		self.driver.find_element_by_id("password").send_keys("12345")
		self.driver.find_element_by_id("login").click()
		self.driver.get(self.live_server_url+"/order/")
		#test model order
		prevcnt=Order.objects.all().count()
		self.driver.find_element_by_id("place-order-btn").click()
		time.sleep(1)
		self.driver.find_element_by_id("orderAddress").send_keys("streettest")
		select = Select(self.driver.find_element_by_id("chooseStore"))
		select.select_by_visible_text(str(self.store.id))
		self.driver.find_element_by_id("order_palce").click()
		time.sleep(1)
		aftercnt=Order.objects.all().count()
		# print("prevcnt is: "+str(prevcnt)+" aftercnt is: "+str(aftercnt))
		self.assertEqual(prevcnt+1,aftercnt)

	def test_store(self):
		print("test_store")
		self.driver = webdriver.Chrome()
		# test authentication of manager
		self.driver.get(self.live_server_url+"/login/")
		self.driver.find_element_by_id("username").send_keys("manager")
		self.driver.find_element_by_id("password").send_keys("12345")
		self.driver.find_element_by_id("login").click()
		self.driver.get(self.live_server_url+"/manage_store/")
		prevcnt=Store.objects.all().count()
		self.driver.find_element_by_id("addStorebtn").click()
		time.sleep(1)
		self.driver.find_element_by_id("addName").send_keys("storetest")
		self.driver.find_element_by_id("addAddress").send_keys("storetest")
		self.driver.find_element_by_id("confirmAdd").click()
		time.sleep(1)
		# test model store
		aftercnt=Store.objects.all().count()
		print("prevcnt is: "+str(prevcnt)+" aftercnt is: "+str(aftercnt))
		self.assertEqual(prevcnt+1,aftercnt)

	def test_role_change(self):
		print("test_role_change")
		# test model User
		self.driver = webdriver.Chrome()
		# test authentication of manager
		self.driver.get(self.live_server_url+"/login/")
		self.driver.find_element_by_id("username").send_keys("manager")
		self.driver.find_element_by_id("password").send_keys("12345")
		self.driver.find_element_by_id("login").click()
		self.driver.get(self.live_server_url+"/manage_role/")
		self.test_user2 = User.objects.create_user(username='testuser2', password='12345') 
		self.test_user2.save()
		self.driver.find_element_by_id("changebtn").click()
		time.sleep(1)
		self.driver.find_element_by_id("changeUserName").send_keys("testuser2")
		select = Select(self.driver.find_element_by_id("groupSelect"))
		select.select_by_visible_text("Manager")
		self.driver.find_element_by_id("rolechangebtn").click()
		time.sleep(1)
		current_group_set = Group.objects.get(user=self.test_user2)
		self.assertEqual(current_group_set.name,"Manager")

	def test_menu(self):
		print("test_menu")
		# test model menu
		self.driver = webdriver.Chrome()
		# test authentication of manager
		self.driver.get(self.live_server_url+"/login/")
		self.driver.find_element_by_id("username").send_keys("manager")
		self.driver.find_element_by_id("password").send_keys("12345")
		self.driver.find_element_by_id("login").click()
		self.driver.get(self.live_server_url+"/manage_menu/")
		prevcnt=Menu.objects.all().count()
		self.driver.find_element_by_id("addStore").click()
		time.sleep(1)
		self.driver.find_element_by_id("addName").send_keys("Dishtest")
		self.driver.find_element_by_id("addPrice").send_keys("2.2")
		self.driver.find_element_by_id("addDes").send_keys("test case")
		self.driver.find_element_by_id("addMenubtn").click()
		time.sleep(1)
		aftercnt=Menu.objects.all().count()
		print("prevcnt is: "+str(prevcnt)+" aftercnt is: "+str(aftercnt))
		self.assertEqual(prevcnt+1,aftercnt)


