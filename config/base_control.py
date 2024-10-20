from sqlalchemy import create_engine, MetaData, update
from dotenv import load_dotenv
import os

load_dotenv('.env') # Cargar variables de entorno
url_basedata = os.getenv("DB_CONNECTION") # toma variable de entorno base de datos

# Creamos engine y la coneccion da la base de datos
engine = create_engine(url_basedata)
meta_data = MetaData() # Instanciamos la metadata para facilitar todas las tablas en la base de datos
