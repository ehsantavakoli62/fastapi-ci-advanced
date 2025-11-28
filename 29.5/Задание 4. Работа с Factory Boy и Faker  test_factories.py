# test_factories.py
import pytest
from factories import ClientFactory, ParkingFactory
from models import db, Client, Parking

def test_create_client_with_factory(db):
    # передаем сессию для Factory Boy
    ClientFactory._meta.sqlalchemy_session = db.session
    client = ClientFactory()
    assert client.id is not None
    assert isinstance(client.name, str)
    assert isinstance(client.surname, str)

def test_create_parking_with_factory(db):
    ParkingFactory._meta.sqlalchemy_session = db.session
    parking = ParkingFactory()
    assert parking.id is not None
    assert parking.count_available_places == parking.count_places
