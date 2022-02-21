import urllib.parse
import requests
from datetime import datetime

print(f'\u001b[6;33;40m{"ADDRESS CONSULT: address, postal-code, city, country "}\u001b[0m')
address = str(input())
address_str = address  # guarda consulta exata sem tratamento
date = (datetime.now().strftime('%d-%m-%Y'))
time = (datetime.now().strftime('%H:%M:%S'))
specialChars = "!#$%:^&,.º*()"
for specialChar in specialChars:
    address = address.replace(specialChar, ' ').lower().title()  # capwords
    address = address.replace('  ', ' ').strip('"')
# address = ''.join(filter(str.isalnum, address))  # remove special chars
# print(address)


def date_input_str():
    date_input = date
    return date_input


def time_input_str():
    time_input = time
    return time_input


def address_input_str():
    address_input = address_str
    return address_input


def get_address(address):
    address_urllib = \
        urllib.parse.quote_plus(address)
    return address_urllib


def parsing_address():
    response = requests.get('http://localhost:4400/parse?address='
                            + get_address(address))
    parsed_address = {}
    for item in response.json():
        parsed_address[item['label']] = item['value']
    return parsed_address


def to_local():  # separa city para comparar com a localidade
    json_parsed_address = parsing_address()
    parsed_address_city = json_parsed_address['city']
    return parsed_address_city
