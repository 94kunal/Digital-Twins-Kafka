import serial
import sys
import time
import json
import pathlib
from utilities import yaml_loadfile
import paho.mqtt.client as client
from kafka import KafkaConsumer
from threading import *
import time

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
        self.ser = serial.Serial('COM3', 9600, timeout=1, parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)

        print("Established Connection with Raspberry Pi Pico Board")

    def get_data(self):

        self.publisher.loop_start()
        while True:

            queue = self.ser.inWaiting()

            if queue > 0:
                self.data = self.ser.read(12)
                self.ser.flushInput()
                self.ser.flushOutput()
                raw_data = [str(self.data, "UTF-8")]

                timestamp = int(round(time.time() * 1000))

                "Get the sensor Decimal values and  decoding it to Temperature and Humidity Values"

                Ambient_Temperature: float = eval(raw_data[0][0:4])

                Ambient_Humidity: float = eval(raw_data[0][6:10])

                Sensor_Data = {"Ambient Temperature": Ambient_Temperature, "Ambient Humidity": Ambient_Humidity,
                               "MQTT_Timestamp": timestamp}

                print(Sensor_Data)
                Sensor_Data_json = json.dumps(Sensor_Data)

                self.publisher.publish(self.details[0]['MQTT']['topic'], Sensor_Data_json)

            self.data = 0
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
