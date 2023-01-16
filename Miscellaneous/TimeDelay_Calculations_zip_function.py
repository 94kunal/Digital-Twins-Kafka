import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from kafka import KafkaConsumer
import pathlib
import yaml
import json
import time
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


class Timestamp_Consumer:

    def __init__(self):
        filepath = pathlib.Path(__file__).resolve().parents[1].joinpath('Config.yaml')
        self.config = yaml_loadfile(filepath)
        self.details = self.config.get('Configurations')

        self.consumer_1 = KafkaConsumer(self.details[1]['KAFKA']['topic'],
                                        bootstrap_servers=[self.details[1]['KAFKA']['broker']],
                                        auto_offset_reset='latest',
                                        group_id=consumer_group_id()
                                        )
        self.consumer_2 = KafkaConsumer(self.details[1]['KAFKA']['Matlab_Topic'],
                                        bootstrap_servers=[self.details[1]['KAFKA']['broker']],
                                        auto_offset_reset='latest',
                                        group_id=consumer_group_id()
                                        )
        self.consumer_3 = KafkaConsumer(self.details[1]['KAFKA']['Java_Direct_Topic'],
                                        bootstrap_servers=[self.details[1]['KAFKA']['broker']],
                                        auto_offset_reset='latest',
                                        group_id=consumer_group_id()
                                        )
        self.client = influxdb_client.InfluxDBClient(url=self.details[2]['INFLUXDB']['host'],
                                                     token=self.details[2]['INFLUXDB']['token'])
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        print("Starting Timestamp Consumer")

    def get_data(self):

        while True:
            for msg, message, message1 in zip(self.consumer_1, self.consumer_2, self.consumer_3):
                timestamp = int(round(time.time() * 1000))
                Sensor_Data = json.loads(msg.value)
                Matlab_Data = json.loads(message.value)
                Java_Model_Data = json.loads(message1.value)
                """Calculating Consumer 1 Time Differences"""

                MQTT_Bridge_Time_diff = (Sensor_Data['Bridge_Timestamp'] - Sensor_Data['MQTT_Timestamp'])
                Bridge_Kafka_Time_diff = (timestamp - Sensor_Data["Bridge_Timestamp"])

                """Calculating Consumer 2 Time Differences"""

                Bridge_Matlab_Time_diff = (Matlab_Data['Matlab_Processed_TimeMs'] - Sensor_Data["Bridge_Timestamp"])
                Matlab_Kafka_Time_diff = (timestamp - Matlab_Data['Matlab_Processed_TimeMs'])

                """Calculating Consumer 3 Time Differences"""

                Bridge_Java_Time_diff = (Java_Model_Data['Java_Processed_Time'] - Sensor_Data["Bridge_Timestamp"])
                Java_Kafka_Time_diff = (timestamp - Java_Model_Data['Java_Processed_Time'])

                """Printing Time Differences of all consumers"""
                print("Current_Time:", timestamp, " MQTT_Bridge_Time_diff:", MQTT_Bridge_Time_diff,
                      " Bridge_Kafka_Time_diff:", Bridge_Kafka_Time_diff, " Bridge_Matlab_Time_diff:",
                      Bridge_Matlab_Time_diff,
                      " Matlab_Kafka_Time_diff:", Matlab_Kafka_Time_diff, " Bridge_Java_Time_diff:",
                      Bridge_Java_Time_diff,
                      " Java_Kafka_Time_diff:", Java_Kafka_Time_diff)

                Timestamp_1 = influxdb_client.Point("Timestamp").tag("location", "Germany") \
                    .field("MQTT Bridge Time Diff", MQTT_Bridge_Time_diff)

                self.write_api.write(self.details[2]['INFLUXDB']['bucket'],
                                     self.details[2]['INFLUXDB']['org'], record=Timestamp_1)

                Timestamp_2 = influxdb_client.Point("Timestamp").tag("location", "Germany") \
                    .field("Bridge_Kafka_Time Diff", Bridge_Kafka_Time_diff)

                self.write_api.write(self.details[2]['INFLUXDB']['bucket'],
                                     self.details[2]['INFLUXDB']['org'], record=Timestamp_2)

                Timestamp_3 = influxdb_client.Point("Timestamp").tag("location", "Germany") \
                    .field("Bridge Matlab Time diff", float(Bridge_Matlab_Time_diff))

                self.write_api.write(self.details[2]['INFLUXDB']['bucket'],
                                     self.details[2]['INFLUXDB']['org'], record=Timestamp_3)

                Timestamp_4 = influxdb_client.Point("Timestamp").tag("location", "Germany") \
                    .field("Matlab Kafka Time diff", float(Matlab_Kafka_Time_diff))

                self.write_api.write(self.details[2]['INFLUXDB']['bucket'],
                                     self.details[2]['INFLUXDB']['org'], record=Timestamp_4)

                Timestamp_5 = influxdb_client.Point("Timestamp").tag("location", "Germany") \
                    .field("Bridge Java Time diff", float(Bridge_Java_Time_diff))

                self.write_api.write(self.details[2]['INFLUXDB']['bucket'],
                                     self.details[2]['INFLUXDB']['org'], record=Timestamp_5)

                Timestamp_6 = influxdb_client.Point("Timestamp").tag("location", "Germany") \
                    .field("Java Kafka Time diff", float(Java_Kafka_Time_diff))

                self.write_api.write(self.details[2]['INFLUXDB']['bucket'],
                                     self.details[2]['INFLUXDB']['org'], record=Timestamp_6)


Timestamp_Consumer_object = Timestamp_Consumer()
Timestamp_Consumer_object.get_data()
