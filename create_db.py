from database import Base, engine
from models import Product, Customer, Purchase
import yaml


with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

print("Creating database....")
print(config['DATABASE']['USERNAME'], 
        config['DATABASE']['PASSWORD'],
        config['DATABASE']['HOST'],
        config['DATABASE']['PORT'])

Base.metadata.create_all(engine)
