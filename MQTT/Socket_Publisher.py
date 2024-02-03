import json
import pathlib
from utilities import yaml_loadfile
import paho.mqtt.client as client
from kafka import KafkaConsumer
from threading import *
import time
import socket

def on_connect(client, userdata, flags, rc=0):
    if rc == 0:
        print("Connection to the MQTT-Broker is successful and Publishing Data to MQTT-Broker")
    else:
        print("Bad connection Returned Code =", rc)


def get_lastbit(lastbit):
    if lastbit < 0:
        lastbit = lastbit + 256
        return lastbit
    else:
        return lastbit


class Mqtt_Publisher:

    def __init__(self):

        filepath = pathlib.Path(__file__).resolve().parents[1].joinpath('Config.yaml')
        self.config = yaml_loadfile(filepath)
        self.details = self.config.get('Configurations')
        self.publisher = client.Client("MQTT Python Publisher")
        self.publisher.on_connect = on_connect
        self.publisher.username_pw_set(self.details[0]['MQTT']['username'], self.details[0]['MQTT']['password'])
        self.consumer = KafkaConsumer(self.details[1]['KAFKA']['topic'],
                                      bootstrap_servers=[self.details[1]['KAFKA']['broker']],
                                      auto_offset_reset='latest',
                                      group_id="feedback_control_loop"
                                      )

        self.publisher.connect(self.details[0]['MQTT']['broker'], self.details[0]['MQTT']['port'], keepalive=250)
        print("Established Connection with Raspberry Pi Pico Board")

        " Connection to Socket "
        serverAddress = (self.details[0]['MQTT']['server_ip'], self.details[0]['MQTT']['server_port'])
        self.bufferSize = 1024
        self.UDPClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        while True:
            cmd = "Ready to Receive Readings..."
            cmdEncoded = cmd.encode('utf-8')
            self.UDPClient.sendto(cmdEncoded, serverAddress)
            print("Socket Connection Successful")
            break

    def get_data(self):

        self.publisher.loop_start()
        while True:
            data, address = self.UDPClient.recvfrom(self.bufferSize)
            dataDecoded = data.decode('utf-8')
            timestamp = int(round(time.time() * 1000))
            Data = dataDecoded.split(':')[0].split(" ")

            "Get the sensor Decimal values and  decoding it to Temperature and Humidity Values"

            Sensor_Data = {"Ambient Temperature": float(Data[0]), "Ambient Humidity": float(Data[1]),
                               "MQTT_Timestamp": timestamp}
            print(Sensor_Data)
            Sensor_Data_json = json.dumps(Sensor_Data)

            self.publisher.publish(self.details[0]['MQTT']['topic'], Sensor_Data_json)

            time.sleep(0.2)
            self.publisher.loop_stop()

    def feedback_control(self):
        while True:
            for msg in self.consumer:
                Sensor_Data = json.loads(msg.value)
                if Sensor_Data['Ambient Temperature'] >= 24.0:
                    # self.ser.write(b"on\n")
                    # time.sleep(1)
                    # self.ser.write(b"off\n")
                    # time.sleep(1)
                    # self.ser.write(heater_on_command())
                    print("HEATER TURNING ON AFTER 1 MINUTE!!")


Mqtt_Publisher_object = Mqtt_Publisher()
t1 = Thread(target=Mqtt_Publisher_object.get_data)
t1.start()
t2 = Thread(target=Mqtt_Publisher_object.feedback_control)
t2.start()
