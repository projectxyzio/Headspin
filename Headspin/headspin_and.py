from time import sleep
from datetime import datetime
import random
import traceback
# from typing import Self
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from os import path
import unittest
import argparse
import urllib3
import os
import sys
import time
urllib3.disable_warnings()

import smtplib
import time
import imaplib
import email
import traceback 
import re

ORG_EMAIL = "@gmail.com" 
FROM_EMAIL = "hstest3new" + ORG_EMAIL 
FROM_PWD = "pcag iggk nasd lvdw" 
SMTP_SERVER = "imap.gmail.com" 
SMTP_PORT = 993


root_dir = os.path.dirname(__file__)
lib_dir = os.path.join(root_dir, 'lib')
pages_dir = os.path.join(root_dir, 'pages')
fixture_data_dir = os.path.join(root_dir, 'fixture_data')
sys.path.append(lib_dir)

from hs_api import hsApi



class SampleTest(unittest.TestCase):

	test_name = "Headspin_and"
	KPI_COUNT = 8
	pass_count = 0


#                   ******* Test  Script Function   ************
	#TEST script  part to setup the Capabilites and start the driver
	def setUp(self):
		self.desired_caps = {
		"headspin:capture": True,
		"headspin:initialScreenSize": {
		"width": 1920,
		"height": 1080
		},
		# "udid": "RFCW20WHMXR",
		"browserName": "chrome", 
		"browserVersion": "91.0.4472.77",
		# "browserName": "MicrosoftEdge",
		# "browserVersion": "91.0.864.48",
		"headspin:testName":self.test_name,
		"headspin:newCommandTimeout": 300,
		"headspin:capture.video": True,
		"headspin:capture.network": False,
		"headspin:noReset": False,
		#"headspin:controlLock": True
		#"autoGrantPermissions": True,

		}																							

		#Initializing Kpis
		self.kpi_labels = {}
		self.kpi_labels["device_starts"] = {"start" : None, "end" : None}
		# self.kpi_labels["Upload_Time"] = {"start" : None, "end" : None}
		self.kpi_labels["Session_Record"] = {"start" : None, "end" : None}
		self.kpi_labels["Waterfall"] = {"start" : None, "end" : None}

		self.kpi_labels["team_settings"] = {"start" : None, "end" : None}
		self.kpi_labels["usage"] = {"start" : None, "end" : None}
		self.kpi_labels["remote_controls"] = {"start" : None, "end" : None}
		self.kpi_labels["performance_sessions"] = {"start" : None, "end" : None}
		self.kpi_labels["performance_monitoring"] = {"start" : None, "end" : None}

		self.pass_count=0
		self.data_kpis = {}
		
		# headspin api module object creation
		self.hs_api_call = hsApi(None, access_token)
		try:
			self.hs_api_call.allocate_garafana()
		except:
			pass
		try:
			self.driver = webdriver.Remote(url, self.desired_caps)
		except Exception as e:
			print(e)

		self.wait = WebDriverWait(self.driver,70)
		self.short_wait = WebDriverWait(self.driver, 0.1)
		self.long_wait = WebDriverWait(self.driver, 90)
		self.session_id = self.driver.session_id


	def read_email_from_gmail(self):
		mail = imaplib.IMAP4_SSL(SMTP_SERVER)
		mail.login(FROM_EMAIL, FROM_PWD)
		mail.select('inbox')
		data = mail.search(None, 'ALL')
		mail_ids = data[1]
		id_list = mail_ids[0].split()
		first_email_id = int(id_list[0])
		latest_email_id = int(id_list[-1])
		i = latest_email_id
		data = mail.fetch(str(i), '(RFC822)')
		for response_part in data:
			arr = response_part[0]
			if isinstance(arr, tuple):
				msg = email.message_from_string(str(arr[1], 'utf-8'))
				email_subject = msg['subject']
				email_from = msg['from']
				print('From: ' + email_from + '\n')
				print('Subject: ' + email_subject + '\n')


				# Get the email body
				email_body = ""
				if msg.is_multipart():
					for part in msg.walk():
						content_type = part.get_content_type()
						content_disposition = str(part.get("Content-Disposition"))
						
						if "attachment" not in content_disposition:
							charset = part.get_content_charset()
							email_body = part.get_payload(decode=True).decode(charset, "ignore")
							break
				else:
					charset = msg.get_content_charset()
					email_body = msg.get_payload(decode=True).decode(charset, "ignore")
				# Print the email body
				#print('Body:\n' + email_body + '\n')
		with open('variable.txt', 'w') as f:
			f.write(email_body)
		f.close()
		with open('variable.txt', 'r') as f:
			ab=f.readlines()
			ba=ab[50]
		f.close()
	#print(ba)
		urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ba)
		self.driver.get(urls[0])
		print(urls[0])

			

	def login(self):
		self.status = "Failed Login"
		time.sleep(3)
		try:
			accept = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.hs-button-accept')))     
			time.sleep(1)
			accept.click() 
		except:
			time.sleep(1)
		login_id = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[ng-model="email_address"]')))
		login_id.click()
		login_id.send_keys("hstest3new@gmail.com")
		login_box = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.login-button-label')))
		sleep(5)
		login_box.click()
		#login_box.click()
		sleep(5)
		self.read_email_from_gmail()
		sleep(3)
		
		# self.driver.get('https://login.yahoo.com/')
		# email = self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="username"]')))
		# sleep(5)
		# email.send_keys("hstest3new@gmail.com")
		# time.sleep(95)
		##actions.move_by_offset(2000, 950).click().perform()
		# next = self.wait.until(EC.presence_of_element_located((By.XPATH,'//input[@id="login-signin"]')))
		# next.click()
		# time.sleep(95)
		# password = self.wait.until(EC.presence_of_element_located((By.XPATH,'//input[@type="password"]')))
		# password.click()
		# time.sleep(1)
		# password.send_keys("spinhead@123")
		# time.sleep(10)
		# print(self.driver.window_handles)
		# next1 = self.wait.until(EC.presence_of_element_located((By.XPATH,'//button[@value="Next"]')))
		# next1.click()
		# time.sleep(20)
		# self.driver.get('https://mail.yahoo.com/')
		## mail = self.wait.until(EC.presence_of_element_located((By.XPATH,'//li[@id="ybar-navigation-item-mail"]')))
		## mail.click()
		# time.sleep(10)
		##actions = ActionChains(self.driver)
		## actions.move_by_offset(1000, 263).click().perform() #firefox
		##actions.move_by_offset(431, 70).click().perform()	 #safari	
		# mail_click = self.wait.until(EC.presence_of_element_located((By.XPATH,'(//span[text()="Sort"]//following::span[contains(text(),"Tricentis")])[1]')))																		 # for yahoo sign in
		# mail_click.click()
		# time.sleep(10)
		# login_link = self.wait.until(EC.presence_of_element_located((By.XPATH,'//a[contains(text(),"Login Link")]')))
		# login_link.click()
		time.sleep(8)
		# print(self.driver.window_handles)           
		# window_handles = self.driver.window_handles           																					# switching the window from yahoo mail to Tricentis
		# self.driver.switch_to.window(window_handles[1])
		login_link1 = self.wait.until(EC.presence_of_element_located((By.XPATH,'//div[contains(text(),"Login to HeadSpin")]')))
		login_link1.click()
		time.sleep(15)
		
	def userflow(self):
		self.status = "Failed Useflow"
		time.sleep(5)


		team = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[hs-docs-location="navbar-icon-base.myteam"]')))			# Team settings Menu
		team.click()
		self.kpi_labels["team_settings"]['start'] = int(round(time.time() * 1000))
		self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"TDC Testing Team")]')))			# Team settings Menu
		self.kpi_labels["team_settings"]['end'] = int(round(time.time() * 1000))
		print ("team_settings Time", self.kpi_labels["team_settings"]['end'] - self.kpi_labels["team_settings"]['start'] )
		self.pass_count = self.pass_count + 1
		time.sleep(3)
		self.kpi_labels["team_settings"]['start_sensitivity'] = 0.9
		self.kpi_labels["team_settings"]['end_sensitivity'] = 0.9
		time.sleep(2)
		print("Team Setting")	

		time.sleep(4)
		usage = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[hs-docs-location="navbar-icon-base.usage"]')))			# Usage Menu
		usage.click()
		self.kpi_labels["usage"]['start'] = int(round(time.time() * 1000))
		self.wait.until(EC.presence_of_element_located((By.XPATH,'//div[contains(text(),"Device Usage")]')))		
		self.kpi_labels["usage"]['end'] = int(round(time.time() * 1000))
		print ("usage Time", self.kpi_labels["usage"]['end'] - self.kpi_labels["usage"]['start'] )
		self.pass_count = self.pass_count + 1
		time.sleep(3)
		self.kpi_labels["usage"]['start_sensitivity'] = 0.9
		self.kpi_labels["usage"]['end_sensitivity'] = 0.9
		time.sleep(2)
		print("usage")


		time.sleep(40)
		try:
			self.driver.find_element(By.XPATH, '//button[@id="from-datepicker"]')
			time.sleep(1)
		except:
			time.sleep(15)
		datebox = self.wait.until(EC.presence_of_element_located((By.XPATH, '//button[@id="from-datepicker"]')))
		datebox.click()
		time.sleep(10)
		datepick = self.wait.until(EC.presence_of_element_located((By.XPATH,'//span[contains(text(),"15")]')))
		datepick.click()
		time.sleep(20)
		button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'button[id="visibility-settings__BV_toggle_"]')))
		button.click()
		time.sleep(3)
		total =  self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'label[class="custom-control-label"]')))
		total.click()
		time.sleep(2)
		total.click()
		time.sleep(3)
		device_usage = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"Device Usage")]')))					# Device Usage under Usage Menu
		device_usage.click()
		time.sleep(10)
		hostname = self.wait.until(EC.presence_of_element_located((By.XPATH,'(//tbody/tr[1]/td[2])[1]')))
		ht=hostname.text
		time.sleep(2)
		time.sleep(2)
		select = Select(self.driver.find_element(By.XPATH,'//button[contains(text(),"Filter Devices")]//preceding::select[1]'))
		time.sleep(2)
		select.select_by_index("2")


		time.sleep(3)
		hostname2 = self.wait.until(EC.presence_of_element_located((By.XPATH,'//div[@role="group"]//input[@placeholder="Hostname"]')))
		hostname2.click()
		time.sleep(2)
		hostname2.send_keys(ht)
		time.sleep(5)
		filterbtn = self.wait.until(EC.presence_of_element_located((By.XPATH,'//button[contains(text(),"Filter Devices")]')))
		filterbtn.click()
		time.sleep(7)
		performance = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[hs-docs-location="navbar-icon-base.performance"]')))
		performance.click()		
		
		self.kpi_labels["performance_monitoring"]['start'] = int(round(time.time() * 1000))
		self.wait.until(EC.presence_of_element_located((By.XPATH,'//div[contains(text(),"User Flows")]')))		
		self.kpi_labels["performance_monitoring"]['end'] = int(round(time.time() * 1000))
		print ("performance_monitoring", self.kpi_labels["performance_monitoring"]['end'] - self.kpi_labels["performance_monitoring"]['start'] )
		self.pass_count = self.pass_count + 1
		time.sleep(3)
		self.kpi_labels["performance_monitoring"]['start_sensitivity'] = 0.9
		self.kpi_labels["performance_monitoring"]['end_sensitivity'] = 0.9
		time.sleep(2)
		print("performance_monitoring")
																											 # Performance Monitoring Menu
		time.sleep(15)

		searching = self.wait.until(EC.presence_of_element_located((By.XPATH,'//input[@type="search"]')))
		time.sleep(4)
		searching.send_keys("test1")
		time.sleep(3)	
		try:
			del_btn = self.wait.until(EC.presence_of_element_located((By.XPATH,'//button[@class="btn btn-outline-danger"]')))
			del_btn.click()
			time.sleep(5)
			dlte_userflow = self.wait.until(EC.presence_of_element_located((By.XPATH,'//button[contains(text(),"Delete User Flow")]')))
			dlte_userflow .click()																										# Deleting the "test" Userflow
			time.sleep(15)
		except:
			time.sleep(1)
		new_user_flow = self.wait.until(EC.presence_of_element_located((By.XPATH,'//button[contains(text(),"+ New User Flow")]')))
		new_user_flow.click()
		time.sleep(3)
		enter_name = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'input[placeholder="Enter a name..."]')))
		enter_name.click()
		time.sleep(3)
		enter_name.send_keys("test1")
		time.sleep(3)
		enter_des = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'textarea[placeholder="Enter a description..."]')))
		enter_des.click()
		enter_des.send_keys("test1")
		time.sleep(3)
		create_user_flow = self.wait.until(EC.presence_of_element_located((By.XPATH,'//button[contains(text(),"Create User Flow")]')))
		create_user_flow.click()																										# Creating a new Userflow named test
		time.sleep(3)
		ok = self.wait.until(EC.presence_of_element_located((By.XPATH,'//button[contains(text(),"OK")]')))
		ok.click()
		time.sleep(17)
		performance_session = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[hs-docs-location="navbar-icon-base.sessions-button"]')))
		performance_session.click()	
		
		self.kpi_labels["performance_sessions"]['start'] = int(round(time.time() * 1000))
		self.wait.until(EC.presence_of_element_located((By.XPATH,'//a[@id="waterfall-button-0"]')))		
		self.kpi_labels["performance_sessions"]['end'] = int(round(time.time() * 1000))
		print ("performance_sessions", self.kpi_labels["performance_sessions"]['end'] - self.kpi_labels["performance_sessions"]['start'] )
		self.pass_count = self.pass_count + 1
		time.sleep(3)
		self.kpi_labels["performance_sessions"]['start_sensitivity'] = 0.9
		self.kpi_labels["performance_sessions"]['end_sensitivity'] = 0.9
		time.sleep(2)
		print("performance_sessions")
		
																										# Performance Sessions Menu
		time.sleep(15)
		session_tag = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Enter a Session Tag Key"]')))
		time.sleep(7)
		session_tag.send_keys("host: RZ8TA0F0V7K@dev-in-blr-0-proxy-34-lin.headspin.io")
		time.sleep(7)
		session_tag.send_keys(Keys.ENTER)																								# Sorting all the session ran on Tuesday of the week
		time.sleep(10)
		open_session = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="session-buttons"]//a[@id="waterfall-button-0"]')))
		open_session.click()																											# Opening a session
		time.sleep(5)
		add_user_flow = self.wait.until(EC.presence_of_element_located((By.XPATH,'//div[contains(text(),"Add to User Flow")]')))
		add_user_flow.click()
		time.sleep(3)
		user_flow_name = self.wait.until(EC.presence_of_element_located((By.XPATH,'//div[contains(text(),"None")]')))
		user_flow_name.click()
		time.sleep(4)
		user_flow_name1 =  self.wait.until(EC.presence_of_element_located((By.XPATH, ' //div[@class="hs-select-option-text"and text() ="test1"]')))
		time.sleep(4)
		user_flow_name1.click() 
		time.sleep(4)
		status = self.wait.until(EC.presence_of_element_located((By.XPATH,'//hs-select[@options="status_options"]//div[@class="hs-selected"]')))
		status.click()
		time.sleep(4)
		status1 =  self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="hs-select-option-text"and text() ="Passed"]')))
		status1.click()
		time.sleep(3)
		Add_Session = self.wait.until(EC.presence_of_element_located((By.XPATH,'//span[contains(text(),"Add Session to User Flow")]')))
		Add_Session.click()																											# Adding userflow name as "test" to opened session
		time.sleep(8)
		Update_status = self.wait.until(EC.presence_of_element_located((By.XPATH,'//span[contains(text(),"Update Status")]')))
		Update_status.click()																											# Updating status as "Passed" of Opened session
		time.sleep(7)
		view_userflow = self.wait.until(EC.presence_of_element_located((By.XPATH,'//a[contains(text(),"View User Flow")]')))
		view_userflow.click()																											# Viewing the Userflow named "test" created
		time.sleep(5)
		clsbtn = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.close-button')))
		clsbtn.click()
		time.sleep(4)
		performance.click()																											# Going Back to Performance Monitoring Menu
		time.sleep(15)
		searching = self.wait.until(EC.presence_of_element_located((By.XPATH,'//input[@type="search"]')))
		time.sleep(4)
		searching.send_keys("test1")
		time.sleep(3)
		del_btn = self.wait.until(EC.presence_of_element_located((By.XPATH,'//button[@class="btn btn-outline-danger"]')))
		del_btn.click()
		time.sleep(5)
		dlte_userflow = self.wait.until(EC.presence_of_element_located((By.XPATH,'//button[contains(text(),"Delete User Flow")]')))
		dlte_userflow .click()																										# Deleting the "test" Userflow
		time.sleep(15)
		performance_session.click()																									# Going Back to Performance Sessions Menu
		time.sleep(15)
		#session_tag = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="autocomplete"]//input[@placeholder="Enter a Session Tag Key"]')))
		session_tag = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Enter a Session Tag Key"]')))

		# session_tag.send_keys("app: com.android.chrome" + "\n")
		# time.sleep(3)
		# try:
		# 	self.driver.find_element(By.XPATH, "//span[@class='tag-value' and text()=' Tue ']").is_displayed()
		# 	session_tag.send_keys(Keys.ENTER)
		# except:
		# 	delete_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="delete-button"]')))
		# 	delete_btn.click()

		session_tag.send_keys("user_flow: Test" + "\n")
		time.sleep(4)
		session_tag.send_keys(Keys.ENTER)
		session_tag.send_keys('/')      
			# time.sleep(5)																									# Sorting all the session ran on Tuesday of the week
		time.sleep(6)
		issue = self.wait.until(EC.presence_of_element_located((By.XPATH,'//a[@ng-href="/sessions/6ab39604-f6a6-11ed-9475-0285c5996533"]')))
		issue.click() 																								# Viewing Issue UI of a particular session
		time.sleep(5)
		try:
			clsbtn = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.close-button')))
			clsbtn.click()

		except:
			sleep(1)
	def remotecntrl(self):
		self.status = "Failed Starting the device"
		time.sleep(2)

	

		remote_control = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[hs-docs-location="navbar-icon-base.remotecontrol"]')))
		remote_control.click()	
		self.kpi_labels["remote_controls"]['start'] = int(round(time.time() * 1000))
		self.wait.until(EC.presence_of_element_located((By.XPATH,'//div[contains(text(),"Device Note")]')))		
		self.kpi_labels["remote_controls"]['end'] = int(round(time.time() * 1000))
		print ("remote_controls", self.kpi_labels["remote_controls"]['end'] - self.kpi_labels["remote_controls"]['start'] )
		self.pass_count = self.pass_count + 1
		time.sleep(3)
		self.kpi_labels["remote_controls"]['start_sensitivity'] = 0.9
		self.kpi_labels["remote_controls"]['end_sensitivity'] = 0.9
		time.sleep(2)
		print("remote_controls")
																												# Remote Control Menu
		time.sleep(35)
		search_dev = self.wait.until(EC.presence_of_element_located((By.XPATH,'//input[@placeholder="Search Devices..."]')))
		search_dev.click()
		#try:
			# initializing list
			# a= "RFCRC08KCAX"
			# b= "RZ8TA0F0V7K"
			# c= "RF8M3014S8L"
			
			# test_list = [a ,b, c]
	
			# printing original list
			# print("Original list is : " + str(test_list))
	
			# using random.choice() to
			# get a random number		
		
			# random_num = random.choice(test_list)
	
			# printing random number
			#print("Random selected number is : " + str(random_num))
			#search_dev.send_keys("10AC8E1K3E000RW")																			# Searching a particular Apple device
			# search_dev.send_keys(str(random_num))	
		#except:
		time.sleep(2)
		search_dev.send_keys("RF8M3014S8L")	
		time.sleep(5)																			# Searching a particular Apple device
		try:
			stoping = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[title="stop device"]')))
			stoping.click()
			time.sleep(4)	
		except:
			time.sleep(1)
		start_using = self.wait.until(EC.presence_of_element_located((By.XPATH,'//span[text()="Start"]')))
		start_using.click()	
		self.kpi_labels["device_starts"]['start'] = int(round(time.time() * 1000))	
		time.sleep(12)
		self.kpi_labels["device_starts"]['end'] = int(round(time.time() * 1000))
		time.sleep(3)	
		print ("Device Locking Time", self.kpi_labels["device_starts"]['end'] - self.kpi_labels["device_starts"]['start'] )
		self.pass_count = self.pass_count + 1
		time.sleep(3)
		self.kpi_labels["device_starts"]['start_sensitivity'] = 0.9
		self.kpi_labels["device_starts"]['end_sensitivity'] = 0.9
		time.sleep(2)
		print("Device started")																										
		time.sleep(12)

	def upload(self):
		# remote_control = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[hs-docs-location="navbar-icon-base.remotecontrol"]')))
		# remote_control.click()	
		time.sleep(5)
		# start_1 = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn device-button icon-button mr-1 p-0 btn-primary"]')))
		# start_1.click()
		# closing = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="close-popup-icon"]')))
		# closing.click()
		# time.sleep(4)
		apps = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'svg[aria-label="menu app fill"]')))
		apps.click()																													# Apps Menu
		time.sleep(7)
		try:
			uninstall = self.wait.until(EC.presence_of_element_located((By.XPATH,'//td[text()="Speedtest"]//following::div[1]'))) 
			uninstall.click()																												# Uninstalling the speedtest app installed
			time.sleep(10)
			time.sleep(9)
			uninstall_ok = self.wait.until(EC.presence_of_element_located((By.XPATH,'//button[contains(text(),"Okay")]'))) 
			uninstall_ok.click()																											# Uninstalling the speedtest app installed
			time.sleep(9)
		except:
			time.sleep(1)
			
		upload_app = self.wait.until(EC.presence_of_element_located((By.XPATH,"//input[@type='file']"))) 
		time.sleep(5)
		a = os.getcwd()
		print(a)
		location_of_ipa = self.upload_file()
		print("done ",location_of_ipa)
		upload_app.send_keys(location_of_ipa)
		time.sleep(40)
		okay =  self.wait.until(EC.presence_of_element_located((By.XPATH,'//button[contains(text(),"Okay")]'))) 
		okay .click()
		time.sleep(15)
		uninstall = self.wait.until(EC.presence_of_element_located((By.XPATH,'//td[text()="Speedtest"]//following::div[1]'))) 
		uninstall.click()																												# Uninstalling the speedtest app installed
		time.sleep(10)
		time.sleep(9)
		uninstall_ok = self.wait.until(EC.presence_of_element_located((By.XPATH,'//button[contains(text(),"Okay")]'))) 
		uninstall_ok.click()																											# Uninstalling the speedtest app installed
		time.sleep(9)
		remote_control = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[hs-docs-location="navbar-icon-base.remotecontrol"]')))
		remote_control.click()	
		time.sleep(4)
		try:
			stoping = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[title="stop device"]')))
			stoping.click()
		except:
			time.sleep(1)
		time.sleep(4)	
		
	def upload_file(self):

		CUR_DIR = path.dirname(path.abspath(__file__))
		APP = path.join(CUR_DIR, 'Speedtest.ipa')
		print(APP)
		a = os.getcwd()
		print(a)
		return APP
	
	def screenshot(self):
		self.status = "Failed App Function"
		time.sleep(5)
		screenshot = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'svg[aria-label="camera fill"]')))
		screenshot.click()  
		time.sleep(5)
		screenshot1 = self.wait.until(EC.presence_of_element_located((By.XPATH,'//button[@class="btn btn-primary"]')))
		screenshot1.click()    
		time.sleep(5)
		screenshot2 = self.wait.until(EC.presence_of_element_located((By.XPATH,'//button[@class="btn btn-danger"]')))
		screenshot2.click()  
		time.sleep(5)
		screenshot3 = self.wait.until(EC.presence_of_element_located((By.XPATH,'//button[contains(text(),"Yes, Delete all")]')))
		screenshot3.click()    
		time.sleep(5)
		log = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'svg[aria-label="file earmark text fill"]')))
		log.click()  
		time.sleep(5)
		log1 = self.wait.until(EC.presence_of_element_located((By.XPATH,'//button[@class="btn mr-1 btn-primary"]')))
		log1.click()    
		time.sleep(5)
		try:
			log_check = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'div[class="text-center font-italic"]')))
			assert log_check.text == 'Press "Get Logs" to start streaming logs.'
			print('Logs not printed')
			time.sleep(5)
		except:
			time.sleep(1)
			print('Logs printed')
		log2 = self.wait.until(EC.presence_of_element_located((By.XPATH,'//button[@class="btn mr-1 btn-danger"]')))
		log2.click()  
		time.sleep(5)
		log3 = self.wait.until(EC.presence_of_element_located((By.XPATH,'//button[@class="btn mr-1 btn-outline-danger"]')))
		log3.click()    
		time.sleep(5)

		start = self.wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class="capture-buttons"]//button[@type="button"]//div[@class="icon"]')))
		start.click()																													# Starting the capture
		time.sleep(7)
		with_nw = self.wait.until(EC.presence_of_element_located((By.XPATH,'//button[contains(text(),"With Network")]')))
		with_nw.click()	
		self.wait.until(EC.presence_of_element_located((By.XPATH,'//div[contains(text(),"Starting...")]')))
		self.kpi_labels["Session_Record"]['start'] = int(round(time.time() * 1000))
		stop = self.wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class="hs-table-icon-button solid-green has-tooltip-no-frills"]')))
		self.kpi_labels["Session_Record"]['end'] = int(round(time.time() * 1000))
		stop.click()
		print("Session Recorded")
		time.sleep(25)
		stop1 = self.wait.until(EC.presence_of_element_located((By.XPATH,'//button[contains(text(),"Stop Recording")]')))
		#self.kpi_labels["Session_Record"]['end'] = int(round(time.time() * 1000))
		time.sleep(1)
		print ("Session Record time", self.kpi_labels["Session_Record"]['end'] - self.kpi_labels["Session_Record"]['start'] )
		self.pass_count = self.pass_count + 1
		time.sleep(1)
		self.kpi_labels["Session_Record"]['start_sensitivity'] = 0.999
		self.kpi_labels["Session_Record"]['end_sensitivity'] = 0.9999
		time.sleep(2)
		stop1.click()																													# Stop Recording the session
		time.sleep(20)

		waterfall = self.wait.until(EC.presence_of_element_located((By.XPATH,'//div[contains(text(),"Waterfall UI")]')))
		self.kpi_labels["Waterfall"]['start'] = int(round(time.time() * 1000))	

		waterfall.click()
		print(self.driver.window_handles)   
		window_handles = self.driver.window_handles           																					# switching the window from yahoo mail to Tricentis
		self.driver.switch_to.window(window_handles[1])      
		# b = self.driver.find_element(By.XPATH,"//div[contains(text(),'Waterfall UI')]")
		# self.driver.execute_script("arguments[0].click();", b)			      
		#self.driver.refresh() 
		add_user = self.wait.until(EC.presence_of_element_located((By.XPATH,'//div[contains(text(),"Add to User Flow")]')))

		#time.sleep(12)
		self.kpi_labels["Waterfall"]['end'] = int(round(time.time() * 1000))

		time.sleep(10)
		print ("Waterfall Load Time", self.kpi_labels["Waterfall"]['end'] - self.kpi_labels["Waterfall"]['start'] )

		self.pass_count = self.pass_count + 1
		time.sleep(1)
		print("Waterfall Loaded")
		time.sleep(2)
		self.kpi_labels["Waterfall"]['start_sensitivity'] = 0.999
		self.kpi_labels["Waterfall"]['end_sensitivity'] = 0.90
		self.driver.switch_to.window(window_handles[0]) 
		closing = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="close-popup-icon"]')))
		closing.click()
		time.sleep(4)
		remote_control = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[hs-docs-location="navbar-icon-base.remotecontrol"]')))
		remote_control.click()	
		time.sleep(4)
		try:
			stoping = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[title="stop device"]')))
			stoping.click()
		except:
			time.sleep(1)
		time.sleep(4)	


	#TEST script function  to  call  all the  test script function.
	def test_SampleTest(self):
		print("Starteddddd")
		try:
			#self.driver.get('https://ui.tricentis.headspin.io/login')
			self.driver.get('https://ui-dev.headspin.io/')
			self.login()
			self.userflow()
			self.remotecntrl()
			self.upload()
			#self.screenshot()
			self.status= "Passed"

		finally:
			self.driver.quit()

	#TEST Script Post Processing Function
	def tearDown(self):
		state = "Passed" if "Fail" not in self.status else "Failed"
		#self.driver.execute_script({'headspin:quitSession'}, {'status': state})
		session_url = "https://ui-dev.headspin.io/sessions/" + self.session_id + "/waterfall"
		print("\nURL :", session_url)
		self.get_video_start_timestamp()

		self.wait_for_session_video_becomes_available()
		print("api call")
		self.hs_api_call.update_userflow_status(session_id=self.session_id, status=state)
		# adding labels
		self.add_session_annotations()

		session_data = self.get_general_session_data()

		# adding data to session
		self.hs_api_call.add_session_data(session_data=session_data)

		description_string = ""
		for data in session_data['data']:
			description_string += data['key'] + " : " + str(data['value']) + "\n"
		# adding name and description to session.

		self.hs_api_call.update_session_name_and_description(session_id=self.session_id, name=self.test_name, description=description_string)

		time.sleep(3)
		if not self.hs_api_call.check_dashboard_allocated():
			self.hs_api_call.allocate_dashboard()  
		
		autosync_status , userflow_id = self.hs_api_call.check_auto_sync_on(self.test_name) 
		if not autosync_status:
			self.hs_api_call.turn_on_auto_sync(userflow_id)



#                        ******* FUNCTION  CALLS  ************
	# adding all the captured data to session data which is uploaded the session
	def get_general_session_data(self):
		session_data = {}
		session_data['session_id'] = self.session_id
		session_data['data'] = []
		# app info
		#session_data['data'].append({"key": "bundle_id", "value": self.package})
		session_data['data'].append({"key": 'status', "value": self.status})
		# add time kpi's
		for label_key in self.kpi_labels.keys():
			data = {}
			data['key'] = label_key
			if self.kpi_labels[label_key]['start'] and self.kpi_labels[label_key]['end']:
				start_time = self.kpi_labels[label_key]['start']
				end_time = self.kpi_labels[label_key]['end']
				if start_time and end_time:
					data['value'] = end_time - start_time
					session_data['data'].append(data)
			else:
				data['value'] = -1
				session_data['data'].append(data)


		# add data kpi's
		for key,value in self.data_kpis.items():
			if value:
				session_data['data'].append({"key": key, "value": value })
			else:
				session_data['data'].append({"key": key, "value": -1 })
		return session_data

	#Function call to ADD Session Annotations  
	def add_session_annotations(self):
		for key, value in self.kpi_labels.items():
			print(f"Adding label: {key} \n\t{value}")
			if self.kpi_labels[key]['start'] and self.kpi_labels[key]['end']:

				label_start_time = self.kpi_labels[key]['start'] - self.video_start_timestamp
				
				label_end_time = self.kpi_labels[key]['end'] - self.video_start_timestamp
				start_sensitivity = self.kpi_labels[key].get('start_sensitivity',0.9)
				end_sensitivity = self.kpi_labels[key].get('end_sensitivity',0.9)
				if label_start_time < 0:
					label_start_time = self.video_start_timestamp - self.video_start_timestamp
				#calling Page Load API
				pageload = self.hs_api_call.get_pageloadtime(session_id=self.session_id, name=key, start_time=label_start_time, end_time=label_end_time, start_sensitivity=start_sensitivity, end_sensitivity=end_sensitivity)

				if 'page_load_regions' in list(pageload.keys()) and 'error_msg' not in pageload['page_load_regions'][0]:
					self.kpi_labels[key]['start'] = float(
						pageload['page_load_regions'][0]['start_time'])
					self.kpi_labels[key]['end'] = float(
						pageload['page_load_regions'][0]['end_time'])
				#Calling Session label API     
				self.hs_api_call.add_label(session_id=self.session_id, name=key, category="kpi", start_time=self.kpi_labels[key]['start'], end_time=self.kpi_labels[key]['end'])

	#Function call to get Video Time Stamp
	def get_video_start_timestamp(self):
		t_end = time.time() + 1000.0
		while time.time() < t_end:
			capture_timestamp = self.hs_api_call.get_capture_timestamp(
				self.session_id)
			self.video_start_timestamp = capture_timestamp['capture-started'] * 1000
			if 'capture-complete' in capture_timestamp:
				break
			time.sleep(1)
		return capture_timestamp

	#Function call to check Video Available for Post Processing 
	def wait_for_session_video_becomes_available(self):
		t_end = time.time() + 1200
		while time.time() < t_end:
			status = self.hs_api_call.get_session_video_metadata(self.session_id)
			if status and ("video_duration_ms" in status):
				print("\nVideo Available for Post Processing\n")
				break 

	
	def find_element_from_locator_list(self, locator_list, finding_time = 30):
		t_end = time.time() + finding_time
		while t_end>time.time():
			for locator in (locator_list):
				try:
					element = self.short_wait.until(EC.presence_of_element_located(locator))
					return element,locator
				except:
					pass
		raise Exception(f"Could not find element from the list: {locator_list}")

if __name__ == '__main__':
	# defining Command line arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('--url', '--url', dest='url',
						type=str, nargs='?',
						default=None,
						required=False,
						help="url")
	
	args = parser.parse_args()
	url = args.url
	access_token = url.split('/')[4]
	headers = {'Authorization': 'Bearer {}'.format(access_token)}


suite = unittest.TestLoader().loadTestsFromTestCase(SampleTest)
unittest.TextTestRunner(verbosity=2).run(suite)

