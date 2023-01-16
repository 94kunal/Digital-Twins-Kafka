import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn import preprocessing


def plot_setup(title):
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Temperature')
    plt.show()


class Influxdb_Temperature:

    def __init__(self):
        pass

    def generate_data_frame(self):
        self.df = pd.read_csv(r'filepath')
        print(self.df)
        self.df['Date'] = pd.to_datetime(self.df['Date']).dt.tz_localize(None)
        self.df['Date'] = pd.to_numeric(pd.to_datetime(self.df['Date']))

    def Linear_Prediction_Wall1_temperature(self):
        sns.lmplot(x='Date', y='Temperature', data=self.df, order=2, ci=None)
        self.df.fillna(method='ffill', inplace=True)
        X = np.array(self.df['Date']).reshape(-1, 1)
        y = np.array(self.df['Temperature']).reshape(-1, 1)
        plt.scatter(X, y, color='b')
        plt.show()
        self.df.dropna(inplace=True)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
        model = LinearRegression()
        model.fit(X_train, y_train)
        plt.scatter(X_test, y_test, color='green')
        plt.plot(X_test, model.predict(X_test), color='k', label="Regression Line")
        plot_setup("Linear Regression")
        print("The accuracy of model is", model.score(X_test, y_test))

    def Polynomial_Prediction_Wall1_temperature(self):
        sns.lmplot(x='Date', y='Temperature', data=self.df, order=2, ci=None)
        yp = np.array(self.df.iloc[:, 1:2].values).reshape(-1, 1)
        xp = np.array(self.df.iloc[:, 0:1].values).reshape(-1, 1)
        plt.scatter(xp, yp, color='b')
        plt.show()
        scaler = preprocessing.StandardScaler()
        polyreg_scaled = make_pipeline(PolynomialFeatures(degree=2), scaler, LinearRegression())
        polyreg_scaled.fit(xp, yp)
        plt.scatter(xp, yp, color='green')
        plt.plot(xp, polyreg_scaled.predict(xp), color="black")
        plot_setup('Polynomial Regression')
        plt.show()
        print("The accuracy of model is", polyreg_scaled.score(xp, yp))


Influxdb_Temperature_object = Influxdb_Temperature()
Influxdb_Temperature_object.generate_data_frame()
Influxdb_Temperature_object.Linear_Prediction_Wall1_temperature()
Influxdb_Temperature_object.Polynomial_Prediction_Wall1_temperature()
