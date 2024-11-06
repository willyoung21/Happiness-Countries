from kafka import KafkaConsumer
from sqlalchemy import create_engine, Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import json

load_dotenv()  
DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"


engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Definir el modelo para la tabla happiness_predictions
class HappinessPrediction(Base):
    __tablename__ = 'happiness_predictions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(255))
    region = Column(String(255))
    gdp_per_capita = Column(Float)
    healthy_life_expectancy = Column(Float)
    freedom = Column(Float)
    perceptions_of_corruption = Column(Float)
    generosity = Column(Float)
    predicted_happiness_score = Column(Float)

# Crear tabla en PostgreSQL si no existe
Base.metadata.create_all(engine)

# Configurar consumidor de Kafka
consumer = KafkaConsumer(
    'happiness_predictions',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Consumir mensajes de Kafka y almacenarlos en PostgreSQL
for message in consumer:
    data = message.value
    features = data['features']
    predicted_score = data['predicted_happiness_score']
    
    # Crear instancia de HappinessPrediction
    prediction = HappinessPrediction(
        country=features['Country'],
        region=features['Region'],
        gdp_per_capita=features['GDP_per_Capita'],
        healthy_life_expectancy=features['Healthy_life_expectancy'],
        freedom=features['Freedom'],
        perceptions_of_corruption=features['Perceptions_of_corruption'],
        generosity=features['Generosity'],
        predicted_happiness_score=predicted_score
    )
    
    # Agregar a la sesión y guardar en la base de datos
    session.add(prediction)
    session.commit()

print("Predicciones recibidas y almacenadas en PostgreSQL usando SQLAlchemy.")

# Cerrar la sesión
session.close()
