import influxdb_client
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pathlib
import yaml
from sklearn.tree import DecisionTreeRegressor


def yaml_loadfile(filepath):
    with open(filepath, 'r') as f:
        data = yaml.safe_load(f)
    return data


class Influxdb_Temperature:

    def __init__(self):

        filepath = pathlib.Path(__file__).resolve().parents[1].joinpath('Config.yaml')
        self.config = yaml_loadfile(filepath)
        self.details = self.config.get('Configurations')
        try:
            self.client = influxdb_client.InfluxDBClient(url=self.details[2]['INFLUXDB']['host'],
                                                         token=self.details[2]['INFLUXDB']['token'])

            print("Starting Influx Db Temperature Query")
            self.query_api = self.client.query_api()
        except Exception as e:
            print("Error in Influx db")

    def flux_query(self):

        self.query = ''' from(bucket: "Kafka Data")
                                |> range(start: -10h)\
                                |> filter(fn: (r) => r["_measurement"] == "xxx")\
                                |> filter(fn: (r) => r["_field"] == "xxx")\
                                |> filter(fn: (r) => r["location"] == "xxx")'''

    def convert_query_data_to_list(self):

        raw, raw1, raw2 = ([] for i in range(3))
        self.result = self.query_api.query(org=self.details[2]['INFLUXDB']['org'], query=self.query)
        for table in self.result:
            for record in table.records:
                if record.get_field() == "xxx":
                    raw.append((record.get_value(), record.get_time()))
                if record.get_field() == "xxx":
                    raw1.append(record.get_value())
                if record.get_field() == "xxx":
                    raw2.append(record.get_value())
        print("=== influxdb query into dataframe ===")
        df = pd.DataFrame(raw, columns=['xxx', 'Date'], index=None)
        df['Date'] = pd.to_datetime(df.Date.dt.strftime('%d/%m/%y %H:%M:%S'))
        df.insert(1, "xxx", raw1, True)
        df.insert(2, "xxx", raw2, True)
        self.indexdf = df.set_index(['Date'])
        print(self.indexdf)

    def get_data_details(self):

        print(self.indexdf.describe())

    def Prediction_data1(self):

        sns.relplot(x='xxx', y='Date', data=self.indexdf)
        plt.show()
        train = self.indexdf.drop(['xxx'], axis=1)
        test = self.indexdf['xxx']
        X_train, X_test, Y_train, Y_test = train_test_split(train, test, test_size=0.3, random_state=2)
        model = LinearRegression()
        model.fit(X_train, Y_train)
        future_values = model.predict(X_test)
        print("The future Values of xxx is", future_values)
        print("The accuracy of model is", model.score(X_test,Y_test))

    def close_Infuxdb_Client(self):
            self.client.close()


Influxdb_Temperature_object = Influxdb_Temperature()
Influxdb_Temperature_object.flux_query()
Influxdb_Temperature_object.convert_query_data_to_list()
Influxdb_Temperature_object.get_data_details()
Influxdb_Temperature_object.Prediction_data1()
Influxdb_Temperature_object.close_Infuxdb_Client()
