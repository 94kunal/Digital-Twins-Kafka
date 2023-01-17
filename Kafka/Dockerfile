# Dockerfile, Image, Container
FROM python:3.10.6

WORKDIR /usr/src/app

COPY Digital-Twins-Kafka/Kafka/requirements.txt ./
COPY Digital-Twins-Kafka/Config.yaml /usr/src/
COPY Digital-Twins-Kafka/utilities.py ./
COPY Digital-Twins-Kafka/Kafka/Display_Kafka_Consumer.py ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "./Display_Kafka_Consumer.py"]