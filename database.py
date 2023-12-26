from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import yaml


with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)
    
DATABASE_URL = (f"postgresql+psycopg2://{config['DATABASE']['USERNAME']}:{config['DATABASE']['PASSWORD']}"
    f"@{config['DATABASE']['HOST']}:{config['DATABASE']['PORT']}/{config['DATABASE']['NAME']}")


engine = create_engine(
    f"postgresql+psycopg2://{config['DATABASE']['USERNAME']}:{config['DATABASE']['PASSWORD']}" +
    f"@{config['DATABASE']['HOST']}:{config['DATABASE']['PORT']}/{config['DATABASE']['NAME']}".format(
        db_username=config['DATABASE']['USERNAME'], 
        db_password=config['DATABASE']['PASSWORD'],
        db_host=config['DATABASE']['HOST'],
        db_port=config['DATABASE']['PORT'],
    ),
    echo=True
)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)
