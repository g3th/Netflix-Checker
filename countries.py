import requests
from bs4 import BeautifulSoup as soup

page = "https://www.myip.com/"

def find_IP():
	countries = {'United_States':'US', 'United_States':'USA','United_Kingdom':'UK', 'France':'FR'}
	my_ip_request = requests.get(page)
	get_page = soup(my_ip_request.content,'html.parser')
	my_ip_find = get_page.find_all('span',attrs={'id':'ip'})
	my_country_find = get_page.find_all('div', attrs={'class':'info_2'})
	my_ip = str(my_ip_find).split(">")[1].split("<")[0]
	my_country = str(my_country_find).split(">")[1].split("<")[0].replace(" ","_")
	return my_ip, my_country, countries[my_country]
