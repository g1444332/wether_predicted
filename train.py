import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import math
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.optimizers import Adam
from keras.models import load_model


def load_data(file_path):
    data = pd.read_csv(file_path)
    data['datetime'] = pd.to_datetime(data['datetime'])
    data.set_index('datetime', inplace = True)
    return data


def prepare_data(data):
    training_data_len = math.ceil(len(data) * .8)
    train_data = data[:training_data_len].iloc[:, :1]
    test_data = data[training_data_len:].iloc[:, :1]

    dataset_train = train_data.temperatureMean.values
    dataset_train = np.reshape(dataset_train, (-1, 1))

    scaler = MinMaxScaler(feature_range = (0, 1))
    scaled_train = scaler.fit_transform(dataset_train)

    X_train = []
    y_train = []
    for i in range(50, len(scaled_train)):
        X_train.append(scaled_train[i - 50:i, 0])
        y_train.append(scaled_train[i, 0])

    X_train, y_train = np.array(X_train), np.array(y_train)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    dataset_test = test_data.temperatureMean.values.reshape(-1, 1)
    scaled_test = scaler.transform(dataset_test)

    X_test = []
    y_test = []
    for i in range(50, len(scaled_test)):
        X_test.append(scaled_test[i - 50:i, 0])
        y_test.append(scaled_test[i, 0])

    X_test, y_test = np.array(X_test), np.array(y_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    return X_train, y_train, X_test, y_test, scaler, test_data


def forecast_temperature(data, data_range: pd.DatetimeIndex, regressor, X_test, scaler):
    last_X = X_test[-1]
    forecast = []

    print()
    days = len(pd.date_range(start=data.index[-1], end=data_range[0]))
    data_range_days = len(data_range)

    for _ in range(days):
        last_X = np.roll(last_X, -1)

    for _ in range(data_range_days):
        next_pred = regressor.predict(last_X.reshape(1, -1, 1))
        forecast.append(next_pred[0, 0])
        last_X = np.roll(last_X, -1)
        last_X[-1] = next_pred

    forecast_data = scaler.inverse_transform(np.array(forecast).reshape(-1, 1))
    return forecast_data


def plot_forecast(ax, date_range: pd.DatetimeIndex, data, forecast_data, test_data):
    ax.plot(data.index, data.temperatureMean, label = 'Actual Data')
    ax.plot(date_range, forecast_data, label = 'Predict Data',
            linestyle = '--')
    ax.set_xlabel('Дата')
    ax.set_ylabel('Температура')
    ax.set_title('Графік Температур')
    ax.grid(True)

