from influxdb_client import InfluxDBClient
import pathlib
from utilities import yaml_loadfile

filepath = pathlib.Path(__file__).resolve().parents[1].joinpath('Config.yaml')
config = yaml_loadfile(filepath)
details = config.get('Configurations')

client = InfluxDBClient(url=details[2]['INFLUXDB']['host'],
                        token=details[2]['INFLUXDB']['token'])

delete_api = client.delete_api()

"""
Delete Data
"""
start = "2021-11-01T00:00:00Z"
stop = "2022-02-01T00:00:00Z"
delete_api.delete(start, stop, '_measurement="Timestamp"', bucket=details[2]['INFLUXDB']['bucket'], org=details[2]['INFLUXDB']['org'])

"""
Close client
"""
client.close()