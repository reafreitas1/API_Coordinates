from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:123456@localhost:5432/db_coordinates'
db = SQLAlchemy(app)


class TbFirstBase(db.Model):  # (NOT RELATIONAL)
    __tablename__ = "tb_first_base"  # não possui ligação com outra tabela
    # Schema
    id_first_base = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.String(20))
    lng = db.Column(db.String(20))
    street = db.Column(db.String(100))
    postal_code = db.Column(db.String(10))
    city = db.Column(db.String(50))
    country = db.Column(db.String(20))


class TbCttCoordinates(db.Model):  # (NOT RELATIONAL)
    __tablename__ = "tb_ctt_coordinates"  # não possui ligação com outra tabela
    # Schema
    id_ctt_coordinates = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    city = db.Column(db.String(50))
    latitude = db.Column(db.String(30))
    longitude = db.Column(db.String(30))


class TbRequest(db.Model):
    __tablename__ = "tb_request"
    # Schema
    id_request = db.Column(db.Integer, primary_key=True)
    date_request = db.Column(db.String(10))
    time_request = db.Column(db.String(10))
    address_raw_data = db.Column(db.String(100))
    user_id = db.Column(Integer, ForeignKey('tb_user.id_user'))
    address_request_id = db.Column(Integer, ForeignKey('tb_address.id_address'))


class TbUser(db.Model):
    __tablename__ = "tb_user"
    # Schema
    id_user = db.Column(db.Integer, primary_key=True)
    name_user = db.Column(db.String(50))
    authentication_data = db.Column(db.String(50))
    # Relationship
    users = relationship('TbRequest')


class TbAddress(db.Model):
    __tablename__ = "tb_address"
    # Schema
    id_address = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(100))
    house_number = db.Column(db.String(10))
    postal_code = db.Column(db.String(15))
    city = db.Column(db.String(20))
    country = db.Column(db.String(10))
    # Relationship
    addresses = relationship('TbRequest')
    addresses2 = relationship('TbCoordinates')


class TbCoordinates(db.Model):
    __tablename__ = "tb_coordinates"
    # Schema
    id_coordinates = db.Column(db.Integer, primary_key=True)
    address_coord_id = db.Column(db.Integer, ForeignKey('tb_address.id_address'))
    coordinates_source_id = db.Column(db.Integer, ForeignKey('tb_coordinates_source.id_coordinates_source'))
    found_lat = db.Column(db.String(15))
    found_lng = db.Column(db.String(15))


class TbCoordinatesSource(db.Model):
    __tablename__ = "tb_coordinates_source"
    # Schema
    id_coordinates_source = db.Column(db.Integer, primary_key=True)
    service_source = db.Column(db.String(10))
    # Relationship
    coordinates = relationship('TbCoordinates')
