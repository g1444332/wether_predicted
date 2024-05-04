import tensorflow as tf

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Загрузка данны
data = pd.read_csv('data.csv')
data['datetime'] = pd.to_datetime(data['datetime'])
data.set_index('datetime', inplace=True)

# Нормализация данных
scaler = MinMaxScaler(feature_range=(0, 1))
data_scaled = scaler.fit_transform(data[['temperature']])

tf.random.set_seed(13)


# Функция для создания датасета
def create_dataset(dataset, look_back=1):
    X, Y = [], []
    for i in range(len(dataset) - look_back - 1):
        a = dataset[i:(i + look_back), 0]
        X.append(a)
        Y.append(dataset[i + look_back, 0])
    return np.array(X), np.array(Y)


# Подготовка данных
look_back = 1
train = data_scaled[data.index < pd.Timestamp('20240229T2300')]
test = data_scaled[data.index >= pd.Timestamp('20240229T2300')]

X_train, Y_train = create_dataset(train, look_back)
X_test, Y_test = create_dataset(test, look_back)

X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

# Создание модели LSTM
model = Sequential()
model.add(LSTM(50, input_shape=(1, look_back)))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')

# Обучение модели
model.fit(X_train, Y_train, epochs=10, batch_size=32, verbose=2)


# Инициализация последнего значения обучающей выборки для начального прогноза
last_train = X_train[-1].reshape(1, 1, look_back)

# Список для сбора прогнозов
test_predictions = []

# Делаем прогнозы на количество шагов, равное размеру тестовой выборки
for _ in range(len(X_test)):
    current_pred = model.predict(last_train)[0]
    test_predictions.append(current_pred)
    # Обновляем last_train, чтобы содержало последний прогноз
    last_train = np.array([[current_pred]])


last = last_train
pred = []
for _ in range(455):
    current_pred = model.predict(last)[0]
    pred.append(current_pred)
    last = np.array([[current_pred]])


pred = scaler.inverse_transform(pred)


# Обратное преобразование для визуализации
test_predictions = scaler.inverse_transform(test_predictions)
print(test_predictions)
print('------------------')
print(scaler.inverse_transform(test)[:len(test_predictions)])

# Расчет RMSE
rmse = np.sqrt(mean_squared_error(scaler.inverse_transform(test)[:len(test_predictions)], test_predictions))
print(f'RMSE: {rmse:.2f}')


# Визуализация
plt.figure(figsize=(15, 7))
training_data_to_plot = scaler.inverse_transform(train)[look_back:]
actual_dates = data.index[data.index >= pd.Timestamp('20240229T2300')]
plt.plot(data.index[data.index < pd.Timestamp('20240229T2300')][look_back:], training_data_to_plot,
         label='Training Data')
plt.plot(actual_dates[:len(test_predictions)], scaler.inverse_transform(test)[:len(test_predictions)],
         label='Actual October Data')
plt.plot(actual_dates[:len(test_predictions)], test_predictions, label='Predicted October Data', linestyle='--')
plt.title('Comparison of Actual and Predicted Values for October')
plt.xlabel('Date')
plt.ylabel('temperature')
plt.legend()
plt.show()
