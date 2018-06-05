import os
from pprint import pprint
from datetime import datetime, timedelta
from DataCleaner import DataCleaner
from read_json import loadData

import pandas as pd
import numpy as np

# from __future__ import print_function
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K

def cat(x):
    if x <-1:
        return "Ahead of schedule"
    if x > 200:
        return "Very Delayed"
    if x > 100:
        return "Delayed"
    return "On schedule"


def convert_date_and_time_columns(frame):
    """ Convert the datatypes related to time and date to one-hot encoding"""

    frame['RecordedAtTime'] = frame['RecordedAtTime'].astype(str).astype('datetime64[ns]')
    # frame['OriginAimedDepartureTime'] = frame['OriginAimedDepartureTime'].astype(str).astype('datetime64[ns]')
    # frame['DestinationAimedArrivalTime'] = frame['DestinationAimedArrivalTime'].astype(str).astype('datetime64[ns]')

    frame['time_datetime'] = pd.to_datetime(frame['RecordedAtTime'])
    # frame['Quarter'] = frame['time_datetime'].dt.quarter
    # frame['Month'] = frame['time_datetime'].dt.month
    # frame['Weekday'] = frame['time_datetime'].dt.dayofweek
    frame['Hour'] = frame['time_datetime'].dt.hour
    frame['Minute'] = frame['time_datetime'].dt.minute


    frame['Time'] = frame['Hour'].map(str) + ":" + frame['Minute'].astype(str)

    # frame['Weekday'] = frame['Weekday'].astype('category', ordered=True, categories=[0, 1, 2, 3, 4, 5, 6])
    # frame = pd.get_dummies(frame, columns=['Weekday'])
    #
    # frame['Month'] = frame['Month'].astype('category', ordered=True,
    #                                        categories=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    # frame = pd.get_dummies(frame, columns=['Month'])
    #
    # frame['Quarter'] = frame['Quarter'].astype('category', ordered=True, categories=[1, 2, 3, 4])
    # frame = pd.get_dummies(frame, columns=['Quarter'])

    frame['Seconds'] = frame['Hour'] * 60 * 60 + frame['Minute'] * 60

    # frame['OriginAimedDepartureTimeSeconds'] = (pd.to_datetime(
    #     frame['OriginAimedDepartureTime'])).dt.hour * 60 * 60 + (pd.to_datetime(
    #     frame['OriginAimedDepartureTime'])).dt.minute * 60.0

    frame['Seconds'] = frame['Seconds'] / (24.0 * 60.0 * 60.0)

    # frame['OriginAimedDepartureTimeSeconds'] = frame['OriginAimedDepartureTimeSeconds'] / (24.0 * 60.0 * 60.0)

    frame = frame.drop(
        ['time_datetime', 'RecordedAtTime', 'Hour',
         'Minute'], 1)  # Removes the date and time columns
    return frame

def train_keras(frame):


    batch_size = 2024
    num_classes = 4
    epochs = 100

    frame = frame.sample(frac=1)

    categories = list(frame['Line'].unique())
    categories.sort()

    # pprint(frame)

    frame['Line'] = pd.Categorical(frame['Line'],categories=categories,ordered=True)
    x_train = pd.get_dummies(frame,columns=['Line'])

    x_train['Time'] = pd.Categorical(x_train['Time'])
    x_train = pd.get_dummies(x_train,columns=['Time'])

    categories_y = list(frame['Delay_2'].unique())
    categories_y.sort()

    x_train.pop('Delay')
    x_train.pop('Seconds')

    y_labels = (x_train.pop('Delay_2'))
    y_labels = pd.Categorical(y_labels,categories=categories_y,ordered=True)
    y_labels = pd.get_dummies(y_labels)

    pprint(x_train.head())
    pprint(y_labels.head())

    # frame['LineId'] = pd.Categorical(frame['LineId'],categories=categories,ordered=True)
    # x_train = pd.get_dummies(frame,columns=['LineId'])


    # frame['LineId'] = pd.Categorical(frame['LineId'],categories=categories,ordered=True)
    # frame = pd.get_dummies(frame,columns=['LineId'])

    # convert class vectors to binary class matrices
    # y_train = keras.utils.to_categorical(np.array(y_labels), num_classes)
    # y_test = keras.utils.to_categorical(y_test, num_classes)

    x_train = np.array(x_train)
    y_labels = np.array(y_labels)

    model = Sequential()


    model.add(Dense(300,activation='relu',input_shape=(x_train.shape[1],)))

    model.add(Dense(200,activation='relu'))

    model.add(Dense(100,activation='relu'))

    model.add(Dense(num_classes, activation='softmax'))

    # model.compile(loss=keras.losses.categorical_crossentropy,
    #               optimizer=keras.optimizers.Adadelta(),
    #               metrics=['accuracy'])

    model.compile(loss=keras.losses.mean_squared_error, optimizer='sgd',
                  metrics=['accuracy'])

    model.fit(x_train, y_labels,
              batch_size=batch_size,
              epochs=epochs,
              verbose=1,
              validation_data=(x_train, y_labels))
    score = model.evaluate(x_train, y_labels, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])

    predictions = model.predict(x_train, verbose=1)
    for p in range(0, len(x_train)):
        print(categories_y)
        print(str(categories_y[np.argmax(predictions[p])]) + " - " + str(predictions[p]))

        show_delay_prediction(predictions[p],categories_y)


        print("Time: " + str(timedelta(seconds=x_train[p][0]*(24.0 * 60.0 * 60.0))))

        # print(categories_y[np.argmax(predictions[p])])
        # print(x_train[p])
        print(" ")
    # pprint(predictions)


def read_data(filename):
    # print("Reading file " + 'lineBased_september_2017_train.csv')
    print("Reading file " + filename)
    dtypes = {'Weekday': np.int32, 'Hour': np.int32,'Minute': np.int32,'TimeTraveledPercentage':np.float32,'Longitude':np.float32, 'Latitude':np.float32, 'Line':str, 'From':str, 'To':str,
     'Delay':np.float32, 'NextStop':str, 'LineId': np.int32, 'DirectionRef':str,'OriginStopTerminalCode':np.int32,
     'DestinationTerminalCode':np.int32, 'NextStopCode':np.int32, 'VehicleId':np.int32,
     'DistanceBetweenStops':np.float32, 'PercentageBetweenStops':np.float32, 'TripHeadsign':str, 'Heading':np.float32}

    #Parsing the three date columns as date
    # dates = ['OriginAimedDepartureTime', 'RecordedAtTime', 'DestinationAimedArrivalTime']


    return pd.read_csv(filename,
                   header=0,
                   dtype= dtypes#, parse_dates=dates
                  )




def show_delay_prediction(prediction, categories):


    predicted = np.argmax(prediction)
    print("Confidence:")
    for i in range(0, len(categories)):
        line = "    "
        if i == predicted:
            line += "* "
        else:
            line += "- "
        line += str(categories[i]) + ": " + str(round(prediction[i]*100)) + "%"
        print(line)


if __name__ == '__main__':



    pathToBlobs = "data/random_one_day"
    dicts = loadData(pathToBlobs)
    frame = pd.DataFrame(dicts)
    print(frame.shape)
    cleaner = DataCleaner()
    frame = cleaner.clean_data(frame)
    print(frame.shape)
    print(frame.head())

    frame = read_data('data/lineBased_september_2017_train.csv')

    frame_pruned = frame[['Delay','Line','RecordedAtTime']]
    frame_pruned = frame_pruned.dropna()

    pprint(frame_pruned['Line'].unique())

    # frame_pruned['Delay_2'] = pd.cut(frame_pruned['Delay'],3, labels = ["Ahead", "On schedule", "Delayed"])

    # for col in df.columns:
    frame_pruned['Delay_2'] = frame_pruned['Delay'].apply(lambda x: cat(x))
    frame_pruned = convert_date_and_time_columns(frame_pruned)

    print(frame_pruned.head(300))
    train_keras(frame_pruned)
