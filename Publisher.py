import serial
import sys
import yaml
import time
import json
import pathlib
import paho.mqtt.client as client
from kafka import KafkaConsumer
from threading import *


def yaml_loadfile(filepath):
    with open(filepath, 'r') as f:
        data = yaml.safe_load(f)
    return data


def heater_on_command():
    hex_array = []
    heater_on = 0x00
    msg = [0x00, 0x0, 0x0]
    hex_array.insert(0, heater_on)
    command_to_send = []
    for i in range(1, 4):
        hex_array.append(msg[i - 1])
    fill_byte = sum(hex_array) + -sum(hex_array)
    hex_array.insert(4, fill_byte)
    checksum = 256 - sum(hex_array)
    hex_array.insert(5, checksum)
    for i in hex_array:
        command_to_send.append(hex(i))
    result = bytes([int(x, 0) for x in command_to_send])
    return result


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
        self.consumer = KafkaConsumer(self.details[1]['KAFKA']['Heater_Topic'],
                                      bootstrap_servers=[self.details[1]['KAFKA']['broker']],
                                      auto_offset_reset='latest',
                                      group_id="xxx"
                                      )
        try:
            self.publisher.connect(self.details[0]['MQTT']['broker'], self.details[0]['MQTT']['port'], keepalive=250)
            self.ser = serial.Serial('xxx', 38400, timeout=1, parity=serial.PARITY_NONE,
                                     stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)

            print("Established Connection with STM32 Nucleo Board")
        except:
            sys.exit("Error connecting device")

    def get_data(self):

        start_bit = [0, 0, 0, 0]
        self.publisher.loop_start()
        while True:

            queue = self.ser.inWaiting()
            if queue > 0:
                self.data = self.ser.read(100)
                self.ser.flushInput()
                self.ser.flushOutput()
                byte_data = []
                for byte in self.data:
                    byte_data.append(byte)

                if byte_data[0:4] == start_bit:
                    timestamp = int(round(time.time() * 1000))

                    "Get the sensor Decimal values and  decoding it to Temperature and Humidity Values"

                    Ambient_Temperature: float = (byte_data[10] * 256 + get_lastbit(byte_data[11])) / 100

                    Ambient_Humidity: float = (byte_data[12] * 256 + get_lastbit(byte_data[13])) / 100

                    Wall1_Temperature: float = (byte_data[14] * 256 + get_lastbit(byte_data[15])) / 100

                    Wall1_Humidity: float = (byte_data[16] * 256 + get_lastbit(byte_data[17])) / 100

                    Wall2_Temperature: float = (byte_data[18] * 256 + get_lastbit(byte_data[19])) / 100

                    Wall2_Humidity: float = (byte_data[20] * 256 + get_lastbit(byte_data[21])) / 100

                    Sensor_Data = {"Ambient Temperature": Ambient_Temperature, "Ambient Humidity": Ambient_Humidity,
                                   "Wall1 Temperature": Wall1_Temperature, "Wall1 Humidity": Wall1_Humidity,
                                   "Wall2 Temperature": Wall2_Temperature, "Wall2 Humidity": Wall2_Humidity,
                                   "MQTT_Timestamp": timestamp}

                    print(Sensor_Data)
                    Sensor_Data_json = json.dumps(Sensor_Data)

                    self.publisher.publish(self.details[0]['MQTT']['topic'], Sensor_Data_json)

                self.data = 0
                print()
            time.sleep(0.2)
            self.publisher.loop_stop()

    def feedback_control(self):
        while True:
            for msg in self.consumer:
                Sensor_Data = json.loads(msg.value)
                if Sensor_Data['xxx'] == 1:
                    self.ser.write(heater_on_command())
                    print("HEATER TURNING ON AFTER 1 MINUTE!!")


Mqtt_Publisher_object = Mqtt_Publisher()
t1 = Thread(target=Mqtt_Publisher_object.get_data)
t2 = Thread(target=Mqtt_Publisher_object.feedback_control)
t1.start()
t2.start()
