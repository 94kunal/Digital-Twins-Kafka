import influxdb_client
import pathlib
import yaml


class Influxdb_Temperature:

    def __init__(self):

        filepath = pathlib.Path(__file__).resolve().parents[1].joinpath('Config.yaml')
        self.config = self.yaml_loadfile(filepath)
        self.details = self.config.get('Configurations')
        self.client = influxdb_client.InfluxDBClient(url=self.details[2]['INFLUXDB']['host'],
                                                     token=self.details[2]['INFLUXDB']['token'])
        print("Starting Influx Db Temperature Query")
        self.query_api = self.client.query_api()
        self.results = []

    def flux_query(self):

        self.query = ''' from(bucket: "Sensor Kafka Data")
                                |> range(start: -10h, stop: 0h)
                                |> filter(fn: (r) => r["_measurement"] == "Temperature")
                                |> filter(fn: (r) => r["_field"] == "Ambient Temperature")
                                |> filter(fn: (r) => r["location"] == "Germany")'''

    def get_query_data(self):

        self.result = self.query_api.query(org=self.details[2]['INFLUXDB']['org'], query=self.query)
        for table in self.result:
            print("Ambient Temperature of Past 20 minutes")
            for record in table.records:
                self.results.append(record.get_value())
        print("Total Readings", len(self.results))

    def display_data(self):
        print(self.results)

    def clear_data(self):
        self.results.clear()

    def yaml_loadfile(self, filepath):

        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        return data


Influxdb_Temperature_object = Influxdb_Temperature()
Influxdb_Temperature_object.flux_query()
Influxdb_Temperature_object.get_query_data()
Influxdb_Temperature_object.display_data()
# Influxdb_Temperature_object.clear_data()
