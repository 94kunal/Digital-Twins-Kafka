# Dockerfile, Image, Container
FROM python:3.10.6

WORKDIR /usr/src/app

COPY Digital-Twins-Kafka/MQTT-KAFKA/requirements.txt ./
COPY Digital-Twins-Kafka/Config.yaml /usr/src/
COPY Digital-Twins-Kafka/utilities.py ./
COPY Digital-Twins-Kafka/MQTT-KAFKA/MQTT_Kafka_Bridge.py ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "./MQTT_Kafka_Bridge.py"]