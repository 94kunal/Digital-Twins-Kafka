from MQTT.MQTT_publisher import Mqtt_Publisher
from MQTT.MQTT_Kafka_Bridge import Mqtt_Kafka_Bridge
# from Kafka.Display_Kafka_Consumer import Kafka_Consumer, start_display_consumer
# from Influxdb.Kafka_Influxdb import InfluxDB_Consumer, start_influxdb_consumer
from threading import *
import time

if __name__ == '__main__':
    Mqtt_Publisher_object = Mqtt_Publisher()
    t1 = Thread(target=Mqtt_Publisher_object.get_data)
    t1.start()
    t2 = Thread(target=Mqtt_Publisher_object.feedback_control)
    t2.start()

    time.sleep(2)

    Mqtt_Kafka_Bridge_object = Mqtt_Kafka_Bridge()

'''
    Kafka_Consumer_object = Kafka_Consumer()
    Kafka_Consumer_object.get_data()
    time.sleep(2)
#password : kunal, picocamera123

    time.sleep(2)
'''