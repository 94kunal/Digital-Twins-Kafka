from kafka import KafkaConsumer
import pathlib
import json
import time

from utilities import yaml_loadfile, consumer_group_id


class Kafka_Consumer:

    def __init__(self):

        filepath = pathlib.Path(__file__).resolve().parents[1].joinpath('Config.yaml')
        self.config = yaml_loadfile(filepath)
        self.details = self.config.get('Configurations')

        self.consumer = KafkaConsumer(self.details[1]['KAFKA']['topic'],
                                      bootstrap_servers=[self.details[1]['KAFKA']['broker']],
                                      auto_offset_reset='latest',
                                      group_id=consumer_group_id()
                                      )
        print("Starting MQTT-KAFKA Consumer")

    def get_data(self):
        while True:
            for msg in self.consumer:
                timestamp = int(round(time.time() * 1000))
                Sensor_Data = json.loads(msg.value)
                Sensor_Data.update([('Kafka_Timestamp', timestamp)])
                print("Receiving MQTT Message", Sensor_Data)


Kafka_Consumer_object = Kafka_Consumer()
Kafka_Consumer_object.get_data()
