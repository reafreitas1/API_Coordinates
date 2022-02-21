from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy
import in_geolocator
import in_parsing
from db_coordinates_model import TbAddress, TbRequest, TbUser, TbCoordinatesSource, TbCoordinates

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:123456@localhost:5432/db_coordinates'
db = SQLAlchemy(app)


@app.route("/post", methods=["POST"])
def post_tabs():
    id_compare_address = []
    coordenadas = in_geolocator.coord_nominatim()
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

    address_dict = in_parsing.parsing_address()
    address_dict_street = address_dict["road"].capitalize()
    address_dict_house_number = (address_dict["house_number"])
    address_dict_house_number = str([int(s) for s in address_dict_house_number.split() if s.isdigit()])
    address_dict_house_number = address_dict_house_number.replace('{', '').replace('}', '')
    address_dict_city = address_dict["city"].capitalize()
    address_dict_country = address_dict["country"].capitalize()
    compare_tb_address = TbAddress.query.filter_by(street=address_dict["road"]).first()
    if compare_tb_address is None:
        try:
            tb_address = TbAddress(street=address_dict_street,
                                   house_number=address_dict_house_number,
                                   postal_code=address_dict["postal_code"],
                                   city=address_dict_city,
                                   country=address_dict_country)
            db.session.add(tb_address)
            db.session.commit()
            print(f'\u001b[32m{"Commit in tb_address its ok!"}\u001b[0m')
        except Exception as e:
            print(f'\u001b[31m{"Error to commit in tb_address: "}\u001b[0m', e)
            pass
    else:
        id_compare_address = compare_tb_address.id_address
        print(id_compare_address)
        print("Address already exist in tb_address")
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

    address_input = in_parsing.address_input_str()  # grava exatamente como foi o input
    time_input = in_parsing.time_input_str()
    date_input = in_parsing.date_input_str()
    if id_compare_address is None:
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
    else:
        try:
            tb_request = TbRequest(user_id=tb_user.id_user,
                                   time_request=time_input,
                                   address_raw_data=address_input,
                                   address_request_id=id_compare_address,
                                   date_request=date_input)
            db.session.add(tb_request)
            db.session.commit()
            print(f'\u001b[32m{"Commit in tb_request its ok!"}\u001b[0m')
        except Exception as e:
            print(f'\u001b[31m{"Error to commit in tb_request: "}\u001b[0m', e)

    # tb_coordinates ---------------------------------------------------------------------------

    lat = str(coordenadas[0])
    lng = str(coordenadas[1])
    # print(lng)
    # print(type(lng))
    compare_lat = TbCoordinates.query.filter_by(found_lat=lat).first()
    compare_lng = TbCoordinates.query.filter_by(found_lng=lng).first()
    # print(compare_lng)
    # print(type(compare_lng))
    if compare_lat is None and compare_lng is None:
        if id_compare_address is None:
            try:
                tb_coordinates = TbCoordinates(address_coord_id=tb_address.id_address,
                                               coordinates_source_id=tb_coordinates_source.id_coordinates_source,
                                               found_lat=lat,
                                               found_lng=lng)
                db.session.add(tb_coordinates)
                print(f'\u001b[32m{"Commit in tb_coordinates its ok!"}\u001b[0m')
                db.session.commit()
            except Exception as e:
                print(f'\u001b[31m{"Error to commit in tb_coordinates: "}\u001b[0m', e)
        else:
            try:
                tb_coordinates = TbCoordinates(address_coord_id=id_compare_address,
                                               coordinates_source_id=tb_coordinates_source.id_coordinates_source,
                                               found_lat=lat,
                                               found_lng=lng)
                db.session.add(tb_coordinates)
                print(f'\u001b[32m{"Commit in tb_coordinates its ok!"}\u001b[0m')
                db.session.commit()
            except Exception as e:
                print(f'\u001b[31m{"Error to commit in tb_coordinates: "}\u001b[0m', e)
    else:
        print("Coordenadas already exist in tb_coordinates")

    return Response(status=200)


app.run()
