import requests
from geopy.geocoders import Nominatim
import in_compare_local


def coord_nominatim():
    geolocator = Nominatim(user_agent="apiCoordinates")
    address = in_compare_local.replace_city()
    # print("»» Nominatim-> Final Address: " + str(address))
    location = geolocator.geocode(address)
    lat = location.latitude
    lng = location.longitude
    return lat, lng


def coord_google():
    address = in_compare_local.replace_city()
    address = str(address.values())  # string
    with open("/home/refreitas/PycharmProjects/Novo_Coordenadas/Data/apikey_google.txt", "r") as key_google:
        apiKey = key_google.read()
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'
           .format(address.replace(' ', '+'), apiKey))

    try:
        response = requests.get(url)
        resp_json_payload = response.json()
        # print(json.dumps(resp_json_payload, indent=2))
        lat = resp_json_payload['results'][0]['geometry']['location']['lat']
        lng = resp_json_payload['results'][0]['geometry']['location']['lng']
    except Exception as e:
        print('ERROR {}'.format(address), e)
        lat = 0
        lng = 0
    return lat, lng

