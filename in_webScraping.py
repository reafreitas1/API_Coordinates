import requests
from bs4 import BeautifulSoup
import in_parsing


def get_postal_page(cp4, cp3):
    url = "https://www.codigo-postal.pt/?cp4={}&cp3={}".format(cp4, cp3)
    response = requests.get(url)
    rhtml = response.text
    return rhtml


def get_page(url):
    response = requests.get(url)
    rhtml = response.text
    return rhtml


def get_postal_coords(cp4, cp3):
    soup = BeautifulSoup(get_postal_page(cp4, cp3), 'html.parser')
    places = soup.find_all("div", class_="places")
    if len(places) == 0:
        # print('no places')
        return None

    gps_elements = places[0].find_all("span", class_="gps")
    if len(gps_elements) == 0:
        # print('no gps')
        return None
    gps_text = gps_elements[0].get_text()
    split_gps = gps_text.split()
    if len(split_gps) != 2:
        # print("invalid gps string")
        return None
    gps_coords = split_gps[1].split(",")
    if len(gps_coords) != 2:
        # print("no coords in string")
        return get_street_coords(places[0].a['href'])
    gps_obj = {"latitude": gps_coords[0], "longitude": gps_coords[1], 'converter': 'codigo-postal.pt'}
    # print(gps_obj)
    return gps_obj


def get_street_coords(href):
    street_page = get_page("https://www.codigo-postal.pt" + href)
    soup = BeautifulSoup(street_page, 'html.parser')
    geo_info = soup.find_all("div", class_="geoinfo")
    if len(geo_info) == 0:
        return None
    if ',' not in geo_info[0].get_text():
        return None
    geo_info_text = geo_info[0].get_text().split()
    longitude = geo_info_text[-1]
    latitude = geo_info_text[-2].split(',')[0]
    gps_obj = {"latitude": latitude, "longitude": longitude, 'converter': 'codigo-postal.pt/street'}
    return gps_obj


def result_web_scraping():
    # print("web_scraping.result_web_scraping ok")
    json_result = in_parsing.parsing_address()
    string_result = json_result['postal_code']
    print("»» Web Scraping-> Postal Code: " + str(string_result))
    string_split = (string_result.split('-'))
    # result = get_postal_coords("4690", "678")
    result = get_postal_coords(string_split[0], string_split[1])
    if result is not None:
        lng = result['longitude']
        lat = result['latitude']
        # print('---» Novo_Coordenadas Web Scraping:\nLatitude:  {}°\nLongitude: {}°'.format(lat, lng))
        return lat, lng


# result_web_scraping()
