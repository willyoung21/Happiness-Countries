from kafka import KafkaProducer
import pandas as pd
import pickle
import json
import os

# Cargar el modelo entrenado
model_path = os.path.join(os.path.dirname(__file__), '../models/final_happiness_model.pkl')
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# Cargar los datos de prueba
test_data_path = os.path.join(os.path.dirname(__file__), '../data/test_results.csv')
test_data = pd.read_csv(test_data_path)

# Configurar el productor de Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Realizar predicciones y enviarlas a Kafka
for _, row in test_data.iterrows():
    features = row[['Country', 'Region', 'GDP_per_Capita', 'Healthy_life_expectancy', 'Freedom', 
                    'Perceptions_of_corruption', 'Generosity']].to_dict()
    
    # Convierte las características en un DataFrame con una sola fila
    features_df = pd.DataFrame([features])
    
    # Realizar la predicción usando el DataFrame
    prediction = model.predict(features_df)[0]
    
    # Crear mensaje para enviar a Kafka
    message = {
        'features': features,
        'predicted_happiness_score': prediction
    }
    
    # Enviar mensaje al topic de Kafka
    producer.send('happiness_predictions', value=message)

print("Predicciones enviadas a Kafka.")
producer.flush()
producer.close()
