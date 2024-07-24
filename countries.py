import requests
def find_IP():
    page = "http://ip-api.com/json/"
    req = requests.get(page).json()
    country = req['country']
    query = req['query']
    country_code = req['countryCode']
    return query, country, country_code

