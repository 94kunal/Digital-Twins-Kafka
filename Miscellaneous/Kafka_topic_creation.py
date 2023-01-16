from kafka.admin import KafkaAdminClient, NewTopic
import pathlib
from utilities import yaml_loadfile

filepath = pathlib.Path(__file__).resolve().parents[1].joinpath('Config.yaml')
config = yaml_loadfile(filepath)
details = config.get('Configurations')


"""This function creates a topic in Kafka.

   Usage: To use this function in the python code for creation of Kafka topic
   Import: from Kafka_topic import Kafka_topic 
   Then call Kafka_topic()
   Please pass the parameters of the function accordingly.
   By default broker is set to Linux Server which is "85.214.243.254:9092"
   client_id = "test", topic_name = "Test1",  partitions=1, replications=1 
   Link to the resource: 
   https://python.plainenglish.io/how-to-programmatically-create-topics-in-kafka-using-python-d8a22590ecde"""


def Kafka_topic(broker=details[1]['KAFKA']['broker'], client="test", topic_name=details[1]['KAFKA']['topic'],
                partitions=1, replications=1):
    admin_client = KafkaAdminClient(
        bootstrap_servers=broker,
        client_id=client
    )

    topic_list = [NewTopic(name=topic_name, num_partitions=partitions, replication_factor=replications)]
    admin_client.create_topics(new_topics=topic_list, validate_only=False)
