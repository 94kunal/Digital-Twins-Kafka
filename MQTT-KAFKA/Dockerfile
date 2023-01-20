# Dockerfile, Image, Container
FROM python:3.10.6

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY ./Config.yaml /usr/src/
COPY ./utilities.py ./
COPY ./MQTT-KAFKA/MQTT_Kafka_Bridge.py ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "./MQTT_Kafka_Bridge.py"]