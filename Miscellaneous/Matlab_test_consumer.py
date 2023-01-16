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

        filepath = pathlib.Path(__file__).parents[1].joinpath('Config.yaml')
        self.config = yaml_loadfile(filepath)
        self.details = self.config.get('Configurations')

        self.consumer = KafkaConsumer(self.details[1]['KAFKA']['Heater_Topic'],
                                      bootstrap_servers=[self.details[1]['KAFKA']['broker']],
                                      auto_offset_reset='latest',
                                      group_id="consumer-group-i"
                                      )
        print("Starting MQTT-KAFKA Consumer")

    def get_data(self):

        while True:
            for msg in self.consumer:
                Sensor_Data = json.loads(msg.value)
                Sensor_Data.update([('Kafka_Timestamp', msg.timestamp)])
                print("Receiving MQTT Message", Sensor_Data)


Kafka_Consumer_object = Kafka_Consumer()
Kafka_Consumer_object.get_data()
