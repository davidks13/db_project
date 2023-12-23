from faker import Faker
import random
import requests

fake = Faker()

base_url = "http://localhost:8000"  # Update with your actual FastAPI server URL


def generate_fake_unit():
    units = ["kg", "kWh", "gram", "pound", "liter", "ounce", "meter", "yard", "ton", "gallon"]
    return random.choice(units)


def generate_fake_product_name():
    product_names = ["Widget", "Gadget", "Thingamajig", "Doohickey", "Contraption", "Gizmo", "Apparatus"]
    return random.choice(product_names)


def create_customer():
    data = {
        "name": fake.name(),
        "address": fake.address(),
        "mobile_number": fake.phone_number(),
        "contact_person": fake.name(),
    }
    response = requests.post(f"{base_url}/customers/", json=data)
    return response.json()


def create_product():
    data = {
        "product_name": generate_fake_product_name(),
        "manufacturer": fake.company(),
        "units": generate_fake_unit()
    }
    response = requests.post(f"{base_url}/products/", json=data)
    return response.json()


def create_purchase():
    customer_id = random.randint(1, 100)
    product_id = random.randint(1, 100)

    data = {
        "customer_id": customer_id,
        "product_id": product_id,
        "quantity": random.randint(1, 100),
        "estimated_shipment_date": fake.date_this_decade().strftime("%Y-%m-%d"),
        "price_per_unit": round(random.uniform(1.0, 100.0), 2),
    }
    response = requests.post(f"{base_url}/purchases/", json=data)
    return response.json()


for _ in range(100):
    create_customer()
    create_product()

for _ in range(100):
    create_purchase()
