import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from kafka import KafkaConsumer
import pathlib
import yaml
import json


class Matlab_Kafka_Consumer:
    """This class gets the data of Absolute Humidity and the Shelf Life from the matlab model,
       and stores in Time series Data base that is Influxdb
       To start this consumer:
       Run Matlab Consumer:- Matlab_Kafka_AbsHum_shelf_Life.m from Matlab_Kafka/Matlab_Models
       This will start the matlab model for calculation of abs Humidity and shelf life"""


    def __init__(self):

        filepath = pathlib.Path(__file__).resolve().parents[1].joinpath('Config.yaml')
        self.config = self.yaml_loadfile(filepath)
        self.details = self.config.get('Configurations')

        self.consumer = KafkaConsumer(self.details[1]['KAFKA']['Matlab_Topic'],
                                      bootstrap_servers=[self.details[1]['KAFKA']['broker']],
                                      auto_offset_reset='latest',
                                      group_id="consumer-group-d"
                                      )
        self.client = influxdb_client.InfluxDBClient(url=self.details[2]['INFLUXDB']['host'],
                                                     token=self.details[2]['INFLUXDB']['token'])
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        print("Starting Matlab_Kafka-Influxdb Consumer")

    def get_data(self):

        while True:
            for msg in self.consumer:
                Matlab_Data = json.loads(msg.value)

                Absolute_Humidity = influxdb_client.Point("Humidity_Matlab_Model").tag("location", "Germany") \
                    .field("Abs_Humidity", Matlab_Data["Absolute_Humidity"])

                self.write_api.write(self.details[2]['INFLUXDB']['bucket'],
                                     self.details[2]['INFLUXDB']['org'], record=Absolute_Humidity)

                Shelf_Life = influxdb_client.Point("Shelf_Life_Matlab_Model").tag("location", "Germany") \
                    .field("Current_Shelf_Life", float(Matlab_Data["Shelf_Life"]))

                self.write_api.write(self.details[2]['INFLUXDB']['bucket'],
                                     self.details[2]['INFLUXDB']['org'], record=Shelf_Life)

    def yaml_loadfile(self, filepath):

        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        return data


Kafka_Consumer_object = Matlab_Kafka_Consumer()
Kafka_Consumer_object.get_data()
