import pandas as pd
from datetime import datetime


# Base class for data cleaner
class DataCleaner(object):

    def clean_data(self, frame):
        """ Runs through all the rules and applies them to the dataframe"""
        for rule in self._rules:
            frame = rule(self, frame)

        return frame

    def remove_null_rows(self, frame):
        # TODO: add hints and comments
        """Records that are missing values for important key-columns shall be removed.
            What might be absolutely necessary to know for the machine learning?
            Some columns we might be ok with if they are null every now and then
        """
        frame = frame[frame['RecordedAtTime'].notnull()]
        frame = frame[frame['OriginAimedDepartureTime'].notnull()]
        frame = frame[frame['DestinationAimedArrivalTime'].notnull()]
        return frame

    def remove_outliers(self, frame):
        # TODO: add hints and comments
        """"Removes outliers and data missing certain values
            Hints: You have data from one day, or do you?
                    All bus routes are in the Rogaland area, but sometimes the GPS freaks out
                    A too long delay might indicate engine trouble or other abnormalities, make sure to remove it!
                    However, if the bus is way ahead of schedule, that's not right either.
                    What's the distance between two stops anyway?
                    If a bus is driving towards its first station, that should not be counted as it being early.
        """
        frame = frame[frame['RecordedAtTime'].astype(str).astype('datetime64[ns]') > datetime(2017, 1, 1)]
        frame = frame[frame['Latitude'] < 61]
        frame = frame[frame['Longitude'] < 7.3]
        frame = frame[frame['Delay'] > -1000]
        frame = frame[frame['Delay'] < 1000]
        frame = frame[frame['DistanceBetweenStops'] > 0]

        frame = frame[(frame['OriginAimedDepartureTime'] <= frame['RecordedAtTime'])]

        return frame





    def remove_unwanted_columns(self, frame):
        # TODO: add hints and comments
        """Remove irrelevant columns.
            Some columns give us no useful information or can't be interpreted as a parameter to a ML model
        """
        exclude = ['VehicleModes', 'NextStopVisitNumber', 'Position',
                   'From', 'To', 'PercentageBetweenStops', 'DirectionRef',
                   'Heading', 'IsMonitored', 'TripHeadsign', 'NextStop']
        frame.drop(exclude, axis=1, inplace=True)



        return frame

    def remove_duplicate_entries(self, frame):
        # TODO: add hints and comments
        """Removes every duplicated row where every value in the specified columns are the same
            What might be used to identify a duplicated row? Ask yourself:
            * Can there be several messages sent at the same time?
            * Can buses leave or arrive at the same time?
            * Could they be at the same place at the same time?
            * How specific do you need to be with line, lineId or TripID?
        """
        columns = ['DestinationAimedArrivalTime', 'DistanceBetweenStops', 'Longitude', 'Latitude',
                   'OriginAimedDepartureTime',
                   'RecordedAtTime', 'TripId']
        frame = frame.drop_duplicates(columns)
        return frame

    def one_hot_encoding(self, frame):
        """ Converts a column with a set of possible values to the index. This must be done before certain ML techniques such as Neural nets"""

        # Before: ['january','february','january']
        # After: [1,2,1]

        # The column is first converted to a category.
        frame['Month'] = frame['Month'].astype('category', ordered=True,
                                               categories=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        frame = pd.get_dummies(frame, columns=['Month'])

        return frame

    def normalize_values(self, frame):
        """ Normalizing sensorvalues so they are between -1 and 1 """

        for feature_name in frame.columns:
            max_value = frame[feature_name].max()
            min_value = frame[feature_name].min()

            # Normalize between -1 and 1
            frame[feature_name] = 2 * ((frame[feature_name] - min_value) / (max_value - min_value)) - 1  # range [-1,1]

            # Normalize between 0 and 1
            frame[feature_name] = ((frame[feature_name] - min_value) / (max_value - min_value))  # range [0,1]

    def convert_date_and_time_columns(self, frame):
        """ Convert the datatypes related to time and date to one-hot encoding"""

        frame['RecordedAtTime'] = frame['RecordedAtTime'].astype(str).astype('datetime64[ns]')
        frame['OriginAimedDepartureTime'] = frame['OriginAimedDepartureTime'].astype(str).astype('datetime64[ns]')
        frame['DestinationAimedArrivalTime'] = frame['DestinationAimedArrivalTime'].astype(str).astype('datetime64[ns]')

        frame['time_datetime'] = pd.to_datetime(frame['RecordedAtTime'])
        frame['Quarter'] = frame['time_datetime'].dt.quarter
        frame['Month'] = frame['time_datetime'].dt.month
        frame['Weekday'] = frame['time_datetime'].dt.dayofweek
        frame['Hour'] = frame['time_datetime'].dt.hour
        frame['Minute'] = frame['time_datetime'].dt.minute

        frame['Weekday'] = frame['Weekday'].astype('category', ordered=True, categories=[0, 1, 2, 3, 4, 5, 6])
        frame = pd.get_dummies(frame, columns=['Weekday'])

        frame['Month'] = frame['Month'].astype('category', ordered=True,
                                               categories=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        frame = pd.get_dummies(frame, columns=['Month'])

        frame['Quarter'] = frame['Quarter'].astype('category', ordered=True, categories=[1, 2, 3, 4])
        frame = pd.get_dummies(frame, columns=['Quarter'])

        frame['Seconds'] = frame['Hour'] * 60 * 60 + frame['Minute'] * 60

        frame['OriginAimedDepartureTimeSeconds'] = (pd.to_datetime(
            frame['OriginAimedDepartureTime'])).dt.hour * 60 * 60 + (pd.to_datetime(
            frame['OriginAimedDepartureTime'])).dt.minute * 60.0

        frame['Seconds'] = frame['Seconds'] / (24.0 * 60.0 * 60.0)

        frame['OriginAimedDepartureTimeSeconds'] = frame['OriginAimedDepartureTimeSeconds'] / (24.0 * 60.0 * 60.0)

        frame = frame.drop(
            ['time_datetime', 'OriginAimedDepartureTime', 'RecordedAtTime', 'DestinationAimedArrivalTime', 'Hour',
             'Minute'], 1)  # Removes the date and time columns
        return frame

    _rules = [remove_null_rows, remove_outliers, remove_duplicate_entries, remove_unwanted_columns]  # TODO add all rules

