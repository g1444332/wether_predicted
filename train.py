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


data = pd.read_csv('data/data_4_years.csv')
data['datetime'] = pd.to_datetime(data['datetime'])
data.set_index('datetime', inplace=True)

training_data_len = math.ceil(len(data) * .8)
train_data = data[:training_data_len].iloc[:, :1]
test_data = data[training_data_len:].iloc[:, :1]

dataset_train = train_data.temperatureMean.values
dataset_train = np.reshape(dataset_train, (-1, 1))

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_train = scaler.fit_transform(dataset_train)

X_train = []
y_train = []
for i in range(50, len(scaled_train)):
    X_train.append(scaled_train[i - 50:i, 0])
    y_train.append(scaled_train[i, 0])

X_train, y_train = np.array(X_train), np.array(y_train)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

# regressorLSTM = Sequential()
# regressorLSTM.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
# regressorLSTM.add(LSTM(50, return_sequences=False))
# regressorLSTM.add(Dense(25))
# regressorLSTM.add(Dense(1))
#
# regressorLSTM.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics = ["accuracy"])
# regressorLSTM.fit(X_train, y_train, batch_size=1, epochs=12)
# regressorLSTM.save("modelLSTM.h5")
regressorLSTM = load_model("modelLSTM.h5")

dataset_test = test_data.temperatureMean.values.reshape(-1, 1)
scaled_test = scaler.transform(dataset_test)

X_test = []
y_test = []
for i in range(50, len(scaled_test)):
    X_test.append(scaled_test[i - 50:i, 0])
    y_test.append(scaled_test[i, 0])

X_test, y_test = np.array(X_test), np.array(y_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))


last_X = X_test[-1]
forecast = []
for _ in range(30):
    next_pred = regressorLSTM.predict(last_X.reshape(1, -1, 1))
    forecast.append(next_pred[0, 0])
    last_X = np.roll(last_X, -1)
    last_X[-1] = next_pred

plt.figure(figsize=(16, 6))
plt.plot(data.index, data.temperatureMean, label='Actual Data')
plt.plot(pd.date_range(test_data.index[-1], periods=30, freq='D'), scaler.inverse_transform(np.array(forecast).reshape(-1, 1)), label='Predict Data', linestyle='--')
plt.xlabel('Date')
plt.ylabel('Temperature')
plt.title('Temperature Predict')
plt.legend()
plt.show()
