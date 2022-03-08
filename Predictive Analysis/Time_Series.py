import influxdb_client
import pandas as pd
import matplotlib.pylab as plt
from pylab import rcParams
from statsmodels.tsa.seasonal import seasonal_decompose
import numpy as np
import pathlib
import yaml


def yaml_loadfile(filepath):
    with open(filepath, 'r') as f:
        data = yaml.safe_load(f)
    return data


class Influxdb_Temperature:

    def __init__(self):

        self.raw, self.raw1, self.raw2 = ([] for i in range(3))
        filepath = pathlib.Path(__file__).resolve().parents[1].joinpath('Config.yaml')
        self.config = yaml_loadfile(filepath)
        self.details = self.config.get('Configurations')

        try:
            self.client = influxdb_client.InfluxDBClient(url=self.details[2]['INFLUXDB']['host'],
                                                         token=self.details[2]['INFLUXDB']['token'])

            print("Starting Influx Db Temperature Query")
            self.query_api = self.client.query_api()

        except:
            print("Error Connecting to Influx db")

    def flux_query(self):

        self.query = ''' from(bucket: "Kafka Data")
                                |> range(start: -1h)\
                                |> filter(fn: (r) => r["_measurement"] == "xxx")\
                                |> filter(fn: (r) => r["_field"] == "xxx")\
                                |> filter(fn: (r) => r["location"] == "xxx")'''

    def convert_query_data_to_list(self):

        self.result = self.query_api.query(org=self.details[2]['INFLUXDB']['org'], query=self.query)
        for table in self.result:
            for record in table.records:
                if record.get_field() == "xxx":
                    self.raw.append((record.get_value(), record.get_time()))
                if record.get_field() == "xxx":
                    self.raw1.append(record.get_value())
                if record.get_field() == "xxx":
                    self.raw2.append(record.get_value())
        print("=== influxdb query into dataframe ===")
        self.df = pd.DataFrame(self.raw, columns=['xxx', 'Date'], index=None)
        self.df['Date'] = pd.to_datetime(self.df.Date.dt.strftime('%d/%m/%y %H:%M:%S'))
        self.indexdf = self.df.set_index(['Date'])
        print(self.indexdf)

    def data1(self):
        self.df.insert(1, "xxx", self.raw1, True)
        self.indexdf1 = self.df.set_index(['Date'])
        print(self.indexdf1)

    def data2(self):
        self.df.insert(2, "xxx", self.raw2, True)
        self.indexdf2 = self.df.set_index(['Date'])
        print(self.indexdf2)

    def get_particular_dataset(self):
        day_data = self.indexdf['2022-03-01': '2022-04-01']

    def plot_data1(self):
        rcParams['figure.figsize'] = 12, 8
        self.indexdf.plot()
        plt.show()

    def data1_decompose(self):

        self.indexdf_mul_decompose = seasonal_decompose(self.indexdf, model='multiplicative', period=10)
        rcParams['figure.figsize'] = 12, 8
        self.indexdf_mul_decompose.plot()
        plt.show()
        self.indexdf_log = self.indexdf.copy()
        self.indexdf_log['xxx'] = np.log(self.indexdf)

    def compare_Time_series(self):
        plt.subplot(2, 1, 1)
        plt.title("Original Time Series")
        plt.plot(self.indexdf)

        plt.subplot(2, 1, 2)
        plt.title("Log Transformed Time Series")
        plt.plot(self.indexdf_log)
        plt.tight_layout()

        plt.show()

    def close_Infuxdb_Client(self):
        self.client.close()


Influxdb_Temperature_object = Influxdb_Temperature()
Influxdb_Temperature_object.flux_query()
Influxdb_Temperature_object.convert_query_data_to_list()
Influxdb_Temperature_object.data1()
Influxdb_Temperature_object.data2()
Influxdb_Temperature_object.data1_decompose()
Influxdb_Temperature_object.compare_Time_series()
Influxdb_Temperature_object.close_Infuxdb_Client()
