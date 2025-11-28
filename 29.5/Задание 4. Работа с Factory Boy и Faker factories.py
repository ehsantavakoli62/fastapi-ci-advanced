# factories.py
import factory
from faker import Faker
from models import Client, Parking

fake = Faker()

class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session_persistence = "commit"
        sqlalchemy_session = None  # нужно будет передать из фикстуры

    name = factory.LazyFunction(fake.first_name)
    surname = factory.LazyFunction(fake.last_name)
    credit_card = factory.LazyFunction(lambda: fake.credit_card_number() if fake.boolean() else None)
    car_number = factory.LazyFunction(lambda: fake.bothify(text="???###"))

class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session_persistence = "commit"
        sqlalchemy_session = None  # нужно будет передать из фикстуры

    address = factory.LazyFunction(fake.address)
    opened = factory.LazyFunction(lambda: fake.boolean())
    count_places = factory.LazyFunction(lambda: fake.random_int(min=1, max=50))
    count_available_places = factory.LazyAttribute(lambda obj: obj.count_places)
