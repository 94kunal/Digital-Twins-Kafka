import json
import paho.mqtt.client as client
import pathlib
import time
from utilities import yaml_loadfile
from kafka import KafkaProducer


def on_connect(client, userdata, flags, rc=0):
    if rc == 0:
        print("Connection to the MQTT-Broker is successful and Starting MQTT-KAFKA Bridge")
    else:
        print("Bad connection Returned Code =", rc)


def json_serializer(data):
    return json.dumps(data).encode("utf-8")


class Mqtt_Kafka_Bridge:

    def __init__(self):

        filepath = pathlib.Path(__file__).resolve().parents[1].joinpath('Config.yaml')
        self.config = yaml_loadfile(filepath)
        self.details = self.config.get('Configurations')
        self.subscriber = client.Client("MQTT Kafka Bridge")
        self.subscriber.on_connect = on_connect
        self.subscriber.username_pw_set(self.details[0]['MQTT']['username'], self.details[0]['MQTT']['password'])

        try:
            self.subscriber.connect(self.details[0]['MQTT']['broker'], self.details[0]['MQTT']['port'], keepalive=250)
            self.subscriber.subscribe(self.details[0]['MQTT']['topic'])

            self.producer = KafkaProducer(bootstrap_servers=[self.details[1]['KAFKA']['broker']],
                                          value_serializer=json_serializer)
            self.subscriber.on_message = self.on_message
            self.subscriber.loop_forever()

        except:
            print("Error in MQTT-KAFKA Bridge connection")

    def on_message(self, client, userdata, msg):
        timestamp = int(round(time.time() * 1000))
        Sensor_data_json = msg.payload.decode()
        Sensor_data = json.loads(Sensor_data_json)
        Sensor_data.update([('Bridge_Timestamp', timestamp)])
        print("Sending Message To Kafka Consumer", Sensor_data)
        self.producer.send(self.details[1]['KAFKA']['topic'], Sensor_data)


Mqtt_Kafka_Bridge_object = Mqtt_Kafka_Bridge()
