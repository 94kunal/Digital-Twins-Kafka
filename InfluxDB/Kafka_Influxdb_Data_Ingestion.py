import influxdb_client, os
from influxdb_client.client.write_api import SYNCHRONOUS
from kafka import KafkaConsumer
import pathlib
import json
from utilities import yaml_loadfile


class InfluxDB_Consumer:

    def __init__(self):

        filepath = pathlib.Path(__file__).resolve().parents[1].joinpath('Config.yaml')
        self.config = yaml_loadfile(filepath)
        self.details = self.config.get('Configurations')
        try:
            self.consumer = KafkaConsumer(self.details[1]['KAFKA']['topic'],
                                          bootstrap_servers=[self.details[1]['KAFKA']['broker']],
                                          auto_offset_reset='latest',
                                          group_id="consumer-group-b"
                                          )
            self.client = influxdb_client.InfluxDBClient(url=self.details[2]['INFLUXDB']['host'],
                                                         token=os.environ.get("INFLUXDB_TOKEN"),
                                                         org=self.details[2]['INFLUXDB']['org'])
            self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
            print("Starting KAFKA-Influxdb Consumer")

        except:
            print("Error in establishing InfluxDB and Kafka Pipeline")

    def get_data(self):

        while True:
            for msg in self.consumer:
                Sensor_Data = json.loads(msg.value)
                Temperature = influxdb_client.Point("Temperature").tag("location", "Germany") \
                    .field("Ambient Temperature", Sensor_Data["Ambient Temperature"])

                self.write_api.write(self.details[2]['INFLUXDB']['bucket'],
                                     self.details[2]['INFLUXDB']['org'], record=Temperature)

                Humidity = influxdb_client.Point("Humidity").tag("location", "Germany") \
                    .field("Ambient Humidity", Sensor_Data["Ambient Humidity"])

                self.write_api.write(self.details[2]['INFLUXDB']['bucket'],
                                     self.details[2]['INFLUXDB']['org'], record=Humidity)


InfluxDB_Consumer_object = InfluxDB_Consumer()
InfluxDB_Consumer_object.get_data()
