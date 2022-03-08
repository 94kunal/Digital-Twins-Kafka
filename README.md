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
    - MQTT_Kafka_Bridge.py: It subcribes to the MQTT topic and send the received data to Kafka Broker.
  
2. Kafka
    - Display_Kafka_Consumer.py: It consumes data from a Kafka topic and prints out the data.
    - TimeDelay_Calculations.py: It consumes data from various Kafka Consumers and calculates the time delays betwwen various software components in different model Interfaces
   
3. InfluxDB:
    - Kafka_Influxdb_Data_Ingestion.py: It consumes data from Kafka topic and puts it to time series database, InfluxDB.
    
4. Predictive_Analysis:
    - Linear_Regression_Model.py: It queries data from InfluxDB and calculates the future values using Linear Regression model.
    - Time_Series.py: It queries data from InfluxDB and calculates seasonality, trend from the data and also decomposes the data. 

5. Config.yaml: It contains the configuration data for the entire Project
