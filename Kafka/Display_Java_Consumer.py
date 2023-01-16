import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from kafka import KafkaConsumer
import pathlib
import yaml
import json
import string
import random


def yaml_loadfile(filepath):
    with open(filepath, 'r') as f:
        data = yaml.safe_load(f)
    return data


def consumer_group_id():
    num_of_string_char = 10
    consumer_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=num_of_string_char))
    return str(consumer_id)


class Kafka_Consumer:

    def __init__(self):

        filepath = pathlib.Path(__file__).resolve().parents[1].joinpath('Config.yaml')
        self.config = yaml_loadfile(filepath)
        self.details = self.config.get('Configurations')

        self.consumer = KafkaConsumer(self.details[1]['KAFKA']['Java_Matlab_Queue_Topic'],
                                      bootstrap_servers=[self.details[1]['KAFKA']['broker']],
                                      auto_offset_reset='latest',
                                      group_id=consumer_group_id()
                                      )

        self.client = influxdb_client.InfluxDBClient(url=self.details[2]['INFLUXDB']['host'],
                                                     token=self.details[2]['INFLUXDB']['token'])
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.delete_api = self.client.delete_api()
        print("Starting MQTT-KAFKA-JAVA Consumer")

    def get_data(self):

        while True:
            for msg in self.consumer:
                Sensor_Data = json.loads(msg.value)
                Sensor_Data.update([('Kafka_Java_Consumer_Timestamp', msg.timestamp)])
                print("Data Received from JAVA-MATLAB Queue: ",
                      "Shelf Life", Sensor_Data["Kafka_Producer_Data"],
                      ", Java Model Reply Time", Sensor_Data["Model_Reply_Time"])


Kafka_Consumer_object = Kafka_Consumer()
Kafka_Consumer_object.get_data()
