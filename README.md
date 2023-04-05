# Digital-Twins-Kafka

Digital twins are virtual representation of physical entity which are continuously updated by real time values.

This example shows how a Digital Twin model can be made using Apache Kafka, InfluxDB and Grafana.

**Prerequistes**

1. Install Eclipse Mosquitto Broker for MQTT protocol communication.
    - https://mosquitto.org/download/
2. Install Zookeeper and Apache Kafka.
    - https://kafka.apache.org/downloads
3. Install InfluxDB
    - https://portal.influxdata.com/downloads/
4. Install Grafana
    - https://grafana.com/grafana/download
 
For ingesting data from InfluxDB to Grafana, No coding is needed.
We need to add InfluxDB query as Data source in Grafana and provide the respective authentication.

Along with Installations, the below Python libraries should also be installed:
  - pyserial, paho-mqtt, influxdb-client, kafka-python, numpy, PyYAML, pandas, matplotlib, statsmodels, seaborn, scikit-learn

After downloading the respective softwares and libaries, edit the config.yaml file with the respective configurations of MQTT Broker,
Kafka Broker and InfluxDB. Some Kafka topics can be excluded from the config file depending on the requirement.

**Explanation**

1. MQTT
    - Publisher.py: Reads data from serial port from STM32 Nucleo board Microcontroller and publishes it to MQTT Broker.
    
2. MQTT-KAFKA
    - MQTT_Kafka_Bridge.py: It subcribes to the MQTT topic and send the received data to Kafka Broker.
  
3. Kafka
    - Display_Kafka_Consumer.py: It consumes data from a Kafka topic and prints out the data.
    - TimeDelay_Calculations.py: It consumes data from various Kafka Consumers and calculates the time delays betwwen various software components in different model Interfaces
   
4. InfluxDB:

    - Kafka_Influxdb_Data_Ingestion.py: It consumes data from Kafka topic and puts it to time series database, InfluxDB.
    
5. Predictive_Analysis:
    - Linear_Regression_Model.py: It queries data from InfluxDB and calculates the future values using Linear Regression model.
    - Time_Series.py: It queries data from InfluxDB and calculates seasonality, trend from the data and also decomposes the data. 

5. Config.yaml: It contains the configuration data for the entire Project

6. docker-compose.yml: The compose file for docker to run the system inside containers.

**Docker Setup**

This project can now be used with Docker.

The indivisual components of the system Apache Kafka, InfluxDB and Grafana can be ran inside different containers using docker-compose.yml file.
Along with the system components, even the Kafka producer, MQTT Bridge, Kafka consumer and InfluxDB data ingestion is created as images and then ran in
different containers.

Each folder containers a Dockerfile and a requirements file which demonstrates how the image is created for the components.

To start the system inside containers:

Since this project is done on ubuntu, download Docker and docker-compose on ubuntu,
Fetch the entire project and run the docker_compose.yml file using: docker-compose up -d (To run it in background)

To run indivisual containers:

Please create the images first using docker-compose.yml file

MQTT -> Publisher.py : 

    docker run -it --rm --network kafka_docker_net -i --device=/dev/ttyACM0 producer-kafka
    device=/dev/ttyACM0 is used since the device is connected to USB port and transferring data. It changes according to USB port used.
    producer-kafka is the name of image.

MQTT-KAFKA -> MQTT_Kafka_Bridge.py:

    docker run -it --rm --network kafka_docker_net -i mqtt-kafka-bridge
    mqtt-kafka-bridge is the name of image.

Kafka -> Display_Kafka_Consumer.py:

    docker run -it --rm --network kafka_docker_net -i consumer-kafka
    consumer-kafka is the name of image.

InfluxDB -> Kafka_Influxdb_data_Ingestion.py:

    docker run -it --rm --network kafka_docker_net -i influxdb-kafka-ingestion
    influxdb-kafka-ingestion is the name of image.

To build indivisual containers out of build context:

    Go to the parent folder, as in this case is PycharmProjects

    docker build -f Digital-Twins/MQTT/Dockerfile -t 'kafka-producer' .
    
    The changes needs to made inside Docker file is:
    
    FROM python:3.10.6
    
    WORKDIR /usr/src/app
    
    COPY Digital-Twins/MQTT/requirements.txt ./
    COPY Digital-Twins/MQTT/Config.yml /usr/src
    COPY Digital-Twins/MQTT/utilities.py ./
    COPY Digital-Twins/MQTT/Publisher.py ./
    
    RUN pip install --no-cache-dir -r requirements.txt
    
    CMD ["python3","./Publisher.py]
    
    Same needs to be done for every other Docker file
    






