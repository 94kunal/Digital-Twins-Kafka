from kafka import KafkaConsumer
import pathlib
import yaml
import json
import time
import random
import string


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
