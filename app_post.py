from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from geopy.geocoders import Nominatim
import urllib.parse
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from db_coordinates_model import TbAddress, TbRequest, TbUser, TbCoordinatesSource, TbCoordinates

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:123456@localhost:5432/db_coordinates'
db = SQLAlchemy(app)


@app.route("/post", methods=["POST"])
def post_tabs():
    address_input = str(request.args.get("address"))

    def date_input_str():
        date = (datetime.now().strftime('%d-%m-%Y'))
        date_in = date
        return date_in

    def time_input_str():
        time = (datetime.now().strftime('%H:%M:%S'))
        time_in = time
        return time_in

    def get_address():
        address1 = ()
        specialChars = "!#$%:^&,.º*()"
        for specialChar in specialChars:
            address1 = address_input.replace(specialChar, ' ').lower().title()
        address2 = address1.replace('  ', ' ').strip('"')
        address_urllib = \
            urllib.parse.quote_plus(address2)
        return address_urllib

    def parsing_address():
        response = requests.get('http://localhost:4400/parse?address='
                                + get_address())
        parsed_address = {}
        for item in response.json():
            parsed_address[item['label']] = item['value']
        return parsed_address

    def find_city():
        parsed_address = parsing_address()
        postcode = parsed_address["postcode"]
        cp_string = postcode
        string_split = (cp_string.split('-'))
        page = ("https://www.codigo-postal.pt/?cp4={}&cp3={}".format(string_split[0], string_split[1]))
        page = requests.get(page)
        soup = BeautifulSoup(page.content, 'html.parser')
        # print(soup.prettify())
        result_local = soup.find_all('span', class_='local')[0].get_text()
        local = str(result_local.split(",")[0])
        parsed_address["city"] = local
        address_final = parsed_address
        return address_final

    address_input_out = find_city()

    def coord_nominatim():
        geolocator = Nominatim(user_agent="apiCoordinates")
        address = address_input_out
        location = geolocator.geocode(address)
        coords_final = location.latitude, location.longitude
        return coords_final

    coordinates = coord_nominatim()
    tb_address = []
    tb_user = []
    tb_coordinates_source = []

    # tb_coordinates_source ---------------------------------------------------------------------

    service = "Nominatim"
    try:
        tb_coordinates_source = TbCoordinatesSource(service_source=service)
        db.session.add(tb_coordinates_source)
        db.session.commit()
        print(f'\u001b[32m{"Commit in tb_coordinates_source its ok!"}\u001b[0m')
    except Exception as e:
        print(f'\u001b[31m{"Error to commit in tb_coordinates_source: "}\u001b[0m', e)

    # tb_address ---------------------------------------------------------------------------

    address_dict = address_input_out
    print(type(address_dict), address_dict)
    address_dict_street = address_dict["road"]
    address_dict_house_number = address_dict["house_number"]
    address_dict_house_number = str([int(s) for s in address_dict_house_number.split() if s.isdigit()])
    address_dict_house_number = address_dict_house_number.replace('{', '').replace('}', '')
    address_dict_city = address_dict["city"]
    address_dict_country = address_dict["country"]
    try:
        tb_address = TbAddress(street=address_dict_street.title(),
                               house_number=address_dict_house_number,
                               postal_code=address_dict["postcode"],
                               city=address_dict_city.title(),
                               country=address_dict_country.title())
        db.session.add(tb_address)
        db.session.commit()
        print(f'\u001b[32m{"Commit in tb_address its ok!"}\u001b[0m')
    except Exception as e:
        print(f'\u001b[31m{"Error to commit in tb_address: "}\u001b[0m', e)
        pass

    # tb_user -----------------------------------------------------------------------------------

    name_user = "Renata Freitas"
    authentication_user = "abc123456789"
    try:
        tb_user = TbUser(name_user=name_user,
                         authentication_data=authentication_user)
        db.session.add(tb_user)
        db.session.commit()
        print(f'\u001b[32m{"Commit in tb_user its ok!"}\u001b[0m')
    except Exception as e:
        print(f'\u001b[31m{"Error to commit in tb_user: "}\u001b[0m', e)

    # tb_request ---------------------------------------------------------------------------------

    time_input = time_input_str()
    date_input = date_input_str()
    try:
        tb_request = TbRequest(user_id=tb_user.id_user,
                               time_request=time_input,
                               address_raw_data=address_input,
                               address_request_id=tb_address.id_address,
                               date_request=date_input)
        db.session.add(tb_request)
        db.session.commit()
        print(f'\u001b[32m{"Commit in tb_request its ok!"}\u001b[0m')
    except Exception as e:
        print(f'\u001b[31m{"Error to commit in tb_request: "}\u001b[0m', e)

    # tb_coordinates ---------------------------------------------------------------------------

    lat_str = str(coordinates[0])
    lng_str = str(coordinates[1])

    try:
        tb_coordinates = TbCoordinates(address_coord_id=tb_address.id_address,
                                       coordinates_source_id=tb_coordinates_source.id_coordinates_source,
                                       found_lat=lat_str,
                                       found_lng=lng_str)
        db.session.add(tb_coordinates)
        print(f'\u001b[32m{"Commit in tb_coordinates its ok!"}\u001b[0m')
        db.session.commit()
    except Exception as e:
        print(f'\u001b[31m{"Error to commit in tb_coordinates: "}\u001b[0m', e)

    return Response(status=200)


app.run()
