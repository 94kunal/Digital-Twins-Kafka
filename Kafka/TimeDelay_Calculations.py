import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from kafka import KafkaConsumer
import pathlib
import yaml
import json
import time
import string
import random
from threading import Thread


def yaml_loadfile(filepath):
    with open(filepath, 'r') as f:
        data = yaml.safe_load(f)
    return data


def consumer_group_id():
    num_of_string_char = 10
    consumer_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=num_of_string_char))
    return str(consumer_id)


class Kafka_Timestamp_Consumer(Thread):

    def __init__(self):
        filepath = pathlib.Path(__file__).resolve().parents[1].joinpath('Config.yaml')
        self.config = yaml_loadfile(filepath)
        self.details = self.config.get('Configurations')

        Thread.__init__(self)
        self.daemon = True

        self.consumer = KafkaConsumer(self.details[1]['KAFKA']['topic'],
                                      bootstrap_servers=[self.details[1]['KAFKA']['broker']],
                                      auto_offset_reset='latest',
                                      group_id=consumer_group_id()
                                      )

        self.client = influxdb_client.InfluxDBClient(url=self.details[2]['INFLUXDB']['host'],
                                                     token=self.details[2]['INFLUXDB']['token'])
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        print("Starting Kafka Timestamp Consumer")
        self.start()

    def run(self):

        while True:

            for msg in self.consumer:
                timestamp = int(round(time.time() * 1000))
                Sensor_Data = json.loads(msg.value)
                MQTT_Bridge_Time_diff = 000
                Bridge_Kafka_Time_diff = 000
                print("Current_Time:", timestamp, " MQTT_Bridge_Time_diff:", MQTT_Bridge_Time_diff,
                      " Bridge_Kafka_Time_diff:", Bridge_Kafka_Time_diff)

                "Putting Timestamp Differences in Influxdb"

                Timestamp_1 = influxdb_client.Point("Timestamp").tag("location", "Germany") \
                    .field("MQTT Bridge Time Diff", MQTT_Bridge_Time_diff)

                self.write_api.write(self.details[2]['INFLUXDB']['bucket'],
                                     self.details[2]['INFLUXDB']['org'], record=Timestamp_1)

                Timestamp_2 = influxdb_client.Point("Timestamp").tag("location", "Germany") \
                    .field("Bridge_Kafka_Time Diff", Bridge_Kafka_Time_diff)

                self.write_api.write(self.details[2]['INFLUXDB']['bucket'],
                                     self.details[2]['INFLUXDB']['org'], record=Timestamp_2)
                print()


class Matlab_Timestamp_Consumer(Thread):

    def __init__(self):
        filepath = pathlib.Path(__file__).resolve().parents[1].joinpath('Config.yaml')
        self.config = yaml_loadfile(filepath)
        self.details = self.config.get('Configurations')
        Thread.__init__(self)
        self.daemon = True

        self.consumer = KafkaConsumer(self.details[1]['KAFKA']['Matlab_Topic'],
                                      bootstrap_servers=[self.details[1]['KAFKA']['broker']],
                                      auto_offset_reset='latest',
                                      group_id=consumer_group_id()
                                      )
        self.client = influxdb_client.InfluxDBClient(url=self.details[2]['INFLUXDB']['host'],
                                                     token=self.details[2]['INFLUXDB']['token'])
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        print("Starting Matlab Timestamp Consumer")
        self.start()

    def run(self):
        for msg in self.consumer:
            timestamp = int(round(time.time() * 1000))
            Matlab_Data = json.loads(msg.value)
            Bridge_Matlab_Time_diff = 000
            Model_Processing_Time = 000
            Matlab_Kafka_Time_diff = 000
            print("Current_Time:", timestamp, " Matlab_Kafka_Time_diff:", Matlab_Kafka_Time_diff
                  , " Bridge_Matlab_Time_diff:", Bridge_Matlab_Time_diff,
                  "ModelProcessing Time", Model_Processing_Time)

            "Putting Timestamp Differences in Influxdb"

            Timestamp_1 = influxdb_client.Point("Timestamp").tag("location", "Germany") \
                .field("Bridge Matlab Time diff", float(Bridge_Matlab_Time_diff))

            self.write_api.write(self.details[2]['INFLUXDB']['bucket'],
                                 self.details[2]['INFLUXDB']['org'], record=Timestamp_1)

            Timestamp_2 = influxdb_client.Point("Timestamp").tag("location", "Germany") \
                .field("Matlab Kafka Time diff", float(Matlab_Kafka_Time_diff))

            self.write_api.write(self.details[2]['INFLUXDB']['bucket'],
                                 self.details[2]['INFLUXDB']['org'], record=Timestamp_2)

            Timestamp_3 = influxdb_client.Point("Timestamp").tag("location", "Germany") \
                .field("Matlab Model Processing Time", float(Model_Processing_Time))

            self.write_api.write(self.details[2]['INFLUXDB']['bucket'],
                                 self.details[2]['INFLUXDB']['org'], record=Timestamp_3)

            print()


class Java_Timestamp_Consumer(Thread):

    def __init__(self):
        filepath = pathlib.Path(__file__).resolve().parents[1].joinpath('Config.yaml')
        self.config = yaml_loadfile(filepath)
        self.details = self.config.get('Configurations')
        Thread.__init__(self)
        self.daemon = True

        self.consumer = KafkaConsumer(self.details[1]['KAFKA']['Java_Direct_Topic'],
                                      bootstrap_servers=[self.details[1]['KAFKA']['broker']],
                                      auto_offset_reset='latest',
                                      group_id=consumer_group_id()
                                      )
        self.client = influxdb_client.InfluxDBClient(url=self.details[2]['INFLUXDB']['host'],
                                                     token=self.details[2]['INFLUXDB']['token'])
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        print("Starting Java Timestamp Consumer")
        self.start()

    def run(self):

        while True:
            for msg in self.consumer:
                timestamp = int(round(time.time() * 1000))
                Java_Model_Data = json.loads(msg.value)
                clock_delay = 900

                Bridge_Java_Time_diff = 000
                Model_Processing_Time = 000
                Java_Kafka_Time_diff = 000
                print("Current_Time:", timestamp, " Java_Kafka_Time_diff:", Java_Kafka_Time_diff,
                      " Bridge_Java_Time_diff:", Bridge_Java_Time_diff,
                      " Model Processing Time", Model_Processing_Time)

                "Putting Timestamp Differences in Influxdb"

                Timestamp_1 = influxdb_client.Point("Timestamp").tag("location", "Germany") \
                    .field("Bridge Java Time diff", float(Bridge_Java_Time_diff))

                self.write_api.write(self.details[2]['INFLUXDB']['bucket'],
                                     self.details[2]['INFLUXDB']['org'], record=Timestamp_1)

                Timestamp_2 = influxdb_client.Point("Timestamp").tag("location", "Germany") \
                    .field("Java Kafka Time diff", float(Java_Kafka_Time_diff))

                self.write_api.write(self.details[2]['INFLUXDB']['bucket'],
                                     self.details[2]['INFLUXDB']['org'], record=Timestamp_2)

                Timestamp_3 = influxdb_client.Point("Timestamp").tag("location", "Germany") \
                    .field("Java Model Processing Time", float(Model_Processing_Time))

                self.write_api.write(self.details[2]['INFLUXDB']['bucket'],
                                     self.details[2]['INFLUXDB']['org'], record=Timestamp_3)
                print()


class Java_Matlab_Consumer(Thread):

    def __init__(self):

        filepath = pathlib.Path(__file__).resolve().parents[1].joinpath('Config.yaml')
        self.config = yaml_loadfile(filepath)
        self.details = self.config.get('Configurations')
        Thread.__init__(self)
        self.daemon = True

        self.consumer = KafkaConsumer(self.details[1]['KAFKA']['Java_Matlab_Queue_Topic'],
                                      bootstrap_servers=[self.details[1]['KAFKA']['broker']],
                                      auto_offset_reset='latest',
                                      group_id=consumer_group_id()
                                      )

        self.client = influxdb_client.InfluxDBClient(url=self.details[2]['INFLUXDB']['host'],
                                                     token=self.details[2]['INFLUXDB']['token'])
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.delete_api = self.client.delete_api()
        print("Starting JAVA-MATLAB Consumer")
        self.start()

    def run(self):

        while True:
            for msg in self.consumer:
                timestamp = int(round(time.time() * 1000))
                Queue_Data = json.loads(msg.value)
                Kafka_Java_Producer_diff = 000
                Matlab_Java_Producer_diff = 000
                Bridge_Java_Consumer_diff = 000
                Java_Matlab_Queue_diff = 000
                print("Current_Time:", timestamp, "Kafka_Java_Matlab_Queue_Time_diff", Kafka_Java_Producer_diff,
                      "Matlab_Java_Producer_diff", Matlab_Java_Producer_diff,
                      "Bridge_Java_Consumer_diff", Bridge_Java_Consumer_diff,
                      "Java_Matlab_Queue_diff", Java_Matlab_Queue_diff)

                "Putting Timestamp Differences in InfluxDb"

                Timestamp_1 = influxdb_client.Point("Timestamp").tag("location", "Germany") \
                    .field("Kafka Java Producer Time diff ", Kafka_Java_Producer_diff)

                self.write_api.write(self.details[2]['INFLUXDB']['bucket'],
                                     self.details[2]['INFLUXDB']['org'], record=Timestamp_1)

                Timestamp_2 = influxdb_client.Point("Timestamp").tag("location", "Germany") \
                    .field("Matlab Java Producer Time diff ", Matlab_Java_Producer_diff)

                self.write_api.write(self.details[2]['INFLUXDB']['bucket'],
                                     self.details[2]['INFLUXDB']['org'], record=Timestamp_2)

                Timestamp_3 = influxdb_client.Point("Timestamp").tag("location", "Germany") \
                    .field("Bridge Java Consumer Time diff ", Bridge_Java_Consumer_diff)

                self.write_api.write(self.details[2]['INFLUXDB']['bucket'],
                                     self.details[2]['INFLUXDB']['org'], record=Timestamp_3)

                Timestamp_4 = influxdb_client.Point("Timestamp").tag("location", "Germany") \
                    .field("Java Matlab Queue Time diff ", Java_Matlab_Queue_diff)

                self.write_api.write(self.details[2]['INFLUXDB']['bucket'],
                                     self.details[2]['INFLUXDB']['org'], record=Timestamp_4)
                print()


Kafka_Timestamp_Consumer()
Matlab_Timestamp_Consumer()
Java_Timestamp_Consumer()
Java_Matlab_Consumer()

while True:
    pass
