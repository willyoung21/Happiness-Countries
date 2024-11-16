# Happiness Prediction Project

This project focuses on predicting the happiness score of different countries using Machine Learning techniques, exploratory data analysis (EDA), feature selection, real-time data streaming with Kafka, and storage in PostgreSQL.

---

## Table of Contents
1. [Project Description](#project-description)
2. [Prerequisites](#prerequisites)
3. [Project Structure](#project-structure)
4. [Environment Setup](#environment-setup)
5. [Data Preparation](#data-preparation)
6. [Model Training](#model-training)
7. [Kafka and PostgreSQL Implementation](#kafka-and-postgresql-implementation)
8. [Kafka Producer and Consumer Execution](#kafka-producer-and-consumer-execution)
9. [Evidence of [Results](#evidence-of-results)
10. [Conclusion](#conclusion)

---

### 1. Project Description <a name="project-description"></a>
This project seeks to predict the happiness index of different countries based on characteristics such as GDP per capita, healthy life expectancy, personal freedom, among other factors. To do this:
- We process happiness data from different years.
- We apply feature selection techniques.
- We train a regression model.
- We use Apache Kafka to transmit the predictions in real time.
- We store the results in PostgreSQL.

### 2. Prerequisites <a name="prerequisites"></a>
- **Python 3.8+**
- **Docker Desktop** for container deployment.
- **Kafka** and **PostgreSQL**.
- **Jupyter Notebook** for EDA and model training.
- Install the following Python packages:

```bash
pip install pandas scikit-learn sqlalchemy kafka-python python-dotenv
```

All dependencies used are in the requirements.txt file.

## 3. Project Structure <a name="project-structure"></a>
The structure of this project is as follows:

### 📁 `data/`
Contains the data files at different stages of processing.

- **`raw/`**: Original data for each year.
- **`processed/`**: Processed data.
- **`clean/`**: Cleaned data ready for analysis.

### 🤖 `models/`
Contains the files related to the trained prediction model.

- **`final_happiness_model.pkl`**: Trained prediction model that predicts the happiness score.

### 💻 `src/`
Contains the source code for data processing and streaming.

- **`kafka_producer.py`**: Kafka producer to send predictions through Kafka.
- **`kafka_consumer.py`**: Kafka consumer to store predictions in PostgreSQL.

### 📓 `notebooks/`
Contains the Jupyter notebooks used for model analysis and training.

- **`eda.ipynb`**: Exploratory analysis of data from 2015 to 2019.
- **`model_training.ipynb`**: Training of the regression model to predict the happiness score.

### 🔧 Configuration files and dependencies

- **`README.md`**: This file contains the project documentation.
- **`docker-compose.yml`**: Configuration of the services for the Kafka broker and ZooKeeper.
- **`requirements.txt`**: Dependencies required to run the project (includes libraries such as `pandas`, `scikit-learn`, `kafka-python`, among others).

---

## 4. create virtual env

python -m venv venv

activate with :

source venv/scripts/activate

## 5. Environment Setup <a name="environment-setup"></a>

Create a .env file in the project root for the PostgreSQL database credentials:

DB_HOST=localhost
DB_NAME=Happiness
DB_USER=postgres
DB_PASSWORD=root
DATABASE_URL=postgresql://user:password@localhost/database_name

## 6. Data Preparation <a name="data-preparation"></a>
The original data is in data/raw. We clean and standardize country names, remove null values.

We open the following notebooks in order and run the cells to perform the cleaning process and save the clean csv files:

notebooks/EDA_2015.ipynb
notebooks/EDA_2016.ipynb
notebooks/EDA_2017.ipynb
notebooks/EDA_2018.ipynb
notebooks/EDA_2019.ipynb

After running them, you should have the clean files in the data/clean folder. Now we run the following notebook to add the region column to the 2017, 2018, and 2019 datasets to later concatenate the data:

notebooks/merge.ipynb

## 7. Model Training <a name="model-training"></a>
Open the notebook notebooks/model_training.ipynb and run the cells to:

Perform feature selection.
Train a regression model to predict the happiness score.
Evaluate and save the model with a satisfactory R² (at least 0.80).
Save the trained model to models/final_happiness_model.pkl.

## 8. Kafka Setup with Docker <a name="Kafka_Setup_with_Docker"></a>

Running the Container

We need to have the Docker desktop application open on our computer and run the command in a git bash in our project

```bash
docker-compose up -d
```

This code will start the container, we can verify it with:

```bash
docker ps
```

Now we will run the following command to create a topic called happiness_predictions:

```bash
docker exec -it happiness-countries-kafka-1 kafka-topics.sh \
--create \
--topic happiness_predictions \
--bootstrap-server localhost:9092 \
--partitions 1 \
--replication-factor 1
```

Now we make sure that the topic was created with this command:

```bash
docker exec -it happiness-countries-kafka-1 kafka-topics.sh \
--list \
--bootstrap-server localhost:9092
```

## 9. Running the Kafka Producer and Consumer <a name="running-the-kafka-producer-and-consumer"></a>

We run the producer script to send predictions to the happiness_predictions topic:

```bash
python src/kafka_producer.py
```

In another terminal, we run the consumer to read the messages and save them in PostgreSQL:

```bash
python src/kafka_consumer.py
```

## 10. Evidence of Results <a name="evidence-of-results"></a>

Verify the predictions in PostgreSQL:

```bash
SELECT * FROM happiness_predictions;
```

## 11. Conclusion <a name="conclusion"></a>
This project provides a complete solution to predict and store happiness scores at a global level, integrating Machine Learning and real-time streaming systems. The architecture built is scalable and allows continuous analysis based on updated happiness data.

## Authors

William Alejandro Botero Florez

This `README.md` has detailed and well-structured instructions that make it easy to navigate and execute the project, covering everything from prerequisites to final implementation.