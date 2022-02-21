import requests
from bs4 import BeautifulSoup
import in_parsing


def find_local():  # procura pelo postal_code no site codigo_postal.pt a localidade atribuída
    json_result = in_parsing.parsing_address()
    string_result = json_result['postal_code']
    string_split = (string_result.split('-'))  # divide a string em tupla
    page = ("https://www.codigo-postal.pt/?cp4={}&cp3={}".format(string_split[0], string_split[1]))
    # print(page)
    page = requests.get(page)
    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup.prettify())
    result_local = soup.find_all('span', class_='local')[0].get_text()
    local = str(result_local.split(",")[0])
    return local

def compare_local():  # substitui a localidade de está diferente
    local_data = in_parsing.to_local().lower()
    local_cp = find_local().lower()
    if local_data != local_cp:
        local_final = local_cp
        # salvar local_final na base de dados sem substituir para a análise
        # print("local_final = local_cp: " + local_final)
        print(f'\u001b[31m{"Changed location: {}".format(local_final)}\u001b[0m')
        return local_final
    else:
        local_final = local_data
        # print("local_final = local_data: " + local_final)
        print(f'\u001b[34m{"Unchanged location: {}".format(local_final)}\u001b[0m')
        return local_final


def replace_city():
    address = in_parsing.parsing_address()  # json
    address['city'] = compare_local()  # troca o city do codigo-postal.pt pelo da pesquisa
    print("Final Address: " + str(address))
    return address
