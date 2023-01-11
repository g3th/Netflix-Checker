import requests
from bs4 import BeautifulSoup as soup

page = "https://www.myip.com/"
countries = {'Canada':'CA','United_States':'US', 'Mexico':'MX','France':'FR','Brazil':'BR','United_Kingdom':'UK', 'France':'FR', 'India':'IN', 'Germany':'DE', 'Australia':'AU', 'Italy':'IT','Romania':'RO','Spain':'ES','Turkey':'TR','Czech_Republic':'CZ','Denmark':'DK','Norway':'NO','Hungary':'HU'}

def find_IP():
	my_ip_request = requests.get(page)
	get_page = soup(my_ip_request.content,'html.parser')
	my_ip_find = get_page.find_all('span',attrs={'id':'ip'})
	my_country_find = get_page.find_all('div', attrs={'class':'info_2'})
	my_ip = str(my_ip_find).split(">")[1].split("<")[0]
	my_country = str(my_country_find).split(">")[1].split("<")[0].replace(" ","_")
	if countries[my_country] == 'UK':
		country_list = ['UK', 'GB']
	elif countries[my_country] == 'US':
		country_list = ['USA', 'US']
		return my_ip, my_country, country_list
	return my_ip, my_country, countries[my_country]
