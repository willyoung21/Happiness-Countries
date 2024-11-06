# Happiness Prediction Project

Este proyecto se centra en predecir el puntaje de felicidad de distintos países utilizando técnicas de Machine Learning, análisis exploratorio de datos (EDA), selección de características, transmisión de datos en tiempo real con Kafka, y almacenamiento en PostgreSQL.

---

## Tabla de Contenidos
1. [Descripción del Proyecto](#descripcion-del-proyecto)
2. [Requisitos Previos](#requisitos-previos)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Configuración del Entorno](#configuracion-del-entorno)
5. [Preparación de los Datos](#preparacion-de-los-datos)
6. [Entrenamiento del Modelo](#entrenamiento-del-modelo)
7. [Implementación de Kafka y PostgreSQL](#implementacion-de-kafka-y-postgresql)
8. [Ejecución del Productor y Consumidor de Kafka](#ejecucion-del-productor-y-consumidor-de-kafka)
9. [Evidencias de Resultados](#evidencias-de-resultados)
10. [Conclusión](#conclusion)

---

### 1. Descripción del Proyecto <a name="descripcion-del-proyecto"></a>
Este proyecto busca predecir el índice de felicidad de diferentes países en base a características como el PIB per cápita, la expectativa de vida saludable, la libertad personal, entre otros factores. Para ello:
- Procesamos datos de felicidad de distintos años.
- Aplicamos técnicas de selección de características.
- Entrenamos un modelo de regresión.
- Utilizamos Apache Kafka para transmitir las predicciones en tiempo real.
- Almacenamos los resultados en PostgreSQL.

### 2. Requisitos Previos <a name="requisitos-previos"></a>
- **Python 3.8+**
- **Docker Desktop** para la implementación de contenedores.
- **Kafka** y **PostgreSQL**.
- **Jupyter Notebook** para EDA y entrenamiento de modelos.
- Instalar los siguientes paquetes de Python:

```bash
pip install pandas scikit-learn sqlalchemy kafka-python python-dotenv
```

Todas las dependencias usadas están en el archivo requirements.txt.

## 3. Estructura del Proyecto <a name="estructura-del-proyecto"></a>
La estructura del proyecto es la siguiente:

├── data
│   ├── raw                  # Datos originales de cada año
│   ├── proccesed            # Datos procesados
│   ├── clean                # Datos limpios
│   └── test_results.csv     # Conjunto de datos para prueba
├── models
│   └── final_happiness_model.pkl   # Modelo de predicción entrenado
├── src
│   ├── kafka_producer.py    # Productor de Kafka para enviar predicciones
│   └── kafka_consumer.py    # Consumidor de Kafka para almacenar predicciones en PostgreSQL
├── notebooks
│   ├── eda.ipynb            # Análisis exploratorio de datos
│   └── model_training.ipynb # Entrenamiento del modelo de regresión
└── README.md                # Este archivo
│  
└──docker-compose.yml        # Servicios para el broker de Kafka y ZooKeeper.
│  
└──requirements.txt          # Dependencias usadas

## 4. create virtual env

python -m venv venv

activate with :

source venv/scripts/activate


## 5. Configuración del Entorno <a name="configuracion-del-entorno"></a>

Crea un archivo .env en la raíz del proyecto para las credenciales de la base de datos PostgreSQL:

DB_HOST=localhost
DB_NAME=Happiness
DB_USER=postgres
DB_PASSWORD=root
DATABASE_URL=postgresql://usuario:contraseña@localhost/nombre_ base_datos

## 6. Preparación de los Datos <a name="preparacion-de-los-datos"></a>
Los datos originales se encuentran en data/raw. Realizamos la limpieza y estandarización de nombres de países, eliminamos valores nulos.

Abrimos los siguientes notebooks en orden y ejecutamos las celdas para realizzar el proceso de limpieza y el gurado de los csv limpios:

notebooks/EDA_2015.ipynb
notebooks/EDA_2016.ipynb
notebooks/EDA_2017.ipynb
notebooks/EDA_2018.ipynb
notebooks/EDA_2019.ipynb

Despues de haberlos ejecutado te debe haber quedado en la carpeta data/clean los archivos limpios, ahora ejecutamos el siguiente notebook para añadir la columna region a los datasets de 2017,2018 y 2019 pra posteriormente hacer la concatenacion de los datos:

notebooks/merge.ipynb


## 7. Entrenamiento del Modelo <a name="entrenamiento-del-modelo"></a>
Abre el notebook notebooks/model_training.ipynb y ejecuta las celdas para:

Realizar la selección de características.
Entrenar un modelo de regresión para predecir el puntaje de felicidad.
Evaluar y guardar el modelo con un R² satisfactorio (al menos 0.80).
Guarda el modelo entrenado en models/final_happiness_model.pkl.

## 8. Configuración de Kafka con Docker <a name="Configuración_de_Kafka_con_Docker"></a>

Ejecución del Contenedor

Tenemos que tener la aplicación de Docker desktop abierta en nuestro ordenador y ejecutamos el comando en un git bash en nuestro proyecto

```bash
docker-compose up -d
```

Este código inicira el contenedor, lo podemos verificar con:

```bash
docker ps
```

Ahora ejecutaremos el siguiente comando para crear un topic llmado happiness_predictions:

```bash
docker exec -it happiness-countries-kafka-1 kafka-topics.sh \
  --create \
  --topic happiness_predictions \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1
```

Ahora nos aseguramos que el topic fue creado con este comando:

```bash
docker exec -it happiness-countries-kafka-1 kafka-topics.sh \
  --list \
  --bootstrap-server localhost:9092
```



## 9.  Ejecución del Productor y Consumidor de Kafka <a name="ejecucion-del-productor-y-consumidor-de-kafka"></a>

Ejecutamos el script del productor para enviar predicciones al topic happiness_predictions:

```bash
python src/kafka_producer.py
```

En otra terminal, ejecutamos el consumidor para leer los mensajes y guardarlos en PostgreSQL:

```bash
python src/kafka_consumer.py
```

## 10.  Evidencias de Resultados <a name="evidencias-de-resultados"></a>

Verifica las predicciones en PostgreSQL:

```bash
SELECT * FROM happiness_predictions;
```

## 11. Conclusión <a name="conclusion"></a>
Este proyecto proporciona una solución completa para predecir y almacenar puntajes de felicidad a nivel global, integrando Machine Learning y sistemas de transmisión en tiempo real. La arquitectura construida es escalable y permite análisis continuos en base a datos actualizados de felicidad.


## Autores

William Alejandro Botero Florez


Este `README.md` tiene instrucciones detalladas y bien estructuradas que facilitan la navegación y ejecución del proyecto, cubriendo desde los requisitos previos hasta la implementación final.


