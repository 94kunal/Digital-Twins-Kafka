import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from kafka import KafkaConsumer
import pathlib
import yaml
import json


def yaml_loadfile(filepath):

    with open(filepath, 'r') as f:
        data = yaml.safe_load(f)
    return data


class Kafka_Consumer:

    def __init__(self):
        filepath = pathlib.Path(__file__).resolve().parents[1].joinpath('Config.yaml')
        self.config = yaml_loadfile(filepath)
        self.details = self.config.get('Configurations')
        self.consumer = KafkaConsumer(self.details[1]['KAFKA']['topic'],
                                      bootstrap_servers=[self.details[1]['KAFKA']['broker']],
                                      auto_offset_reset='latest',
                                      group_id="consumer-group-b"
                                      )
        self.client = influxdb_client.InfluxDBClient(url=self.details[2]['INFLUXDB']['host'],
                                                     token=self.details[2]['INFLUXDB']['token'])
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        print("Starting KAFKA-Influxdb Consumer")

    def get_data(self):

        while True:
            for msg in self.consumer:
                Sensor_Data = json.loads(msg.value)
                Temperature = influxdb_client.Point("xxx").tag("location", "xxx") \
                    .field("xxx", Sensor_Data["xxx"]) \
                    .field("xxx", Sensor_Data["xxx"]) \
                    .field("xxx", Sensor_Data["xxx"])

                self.write_api.write(self.details[2]['INFLUXDB']['bucket'],
                                     self.details[2]['INFLUXDB']['org'], record=xxx)

                Humidity = influxdb_client.Point("xxx").tag("location", "xxx") \
                    .field("xxx", Sensor_Data["xxx"]) \
                    .field("xxx", Sensor_Data["xxx"]) \
                    .field("xxx", Sensor_Data["xxx"])

                self.write_api.write(self.details[2]['INFLUXDB']['bucket'],
                                     self.details[2]['INFLUXDB']['org'], record=xxx)


Kafka_Consumer_object = Kafka_Consumer()
Kafka_Consumer_object.get_data()
