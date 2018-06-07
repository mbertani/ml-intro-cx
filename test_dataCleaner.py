#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime


class TestDataCleaner:
    include = ['RecordedAtTime', 'OriginAimedDepartureTime', 'DestinationAimedArrivalTime', 'NextStop', 'Delay', 'PercentageBetweenStops', 'DestinationAimedArrivalTime',
        'DistanceBetweenStops', 'Longitude', 'Latitude',
        'OriginAimedDepartureTime',
        'RecordedAtTime', 'TripId', 'TripHeadsign']

    def _print_test_failed(self, message):
        print("")
        print("")
        print("\x1b[31mTEST FAILED")
        print(message)
        print("\x1b[0m")

    def _print_test_passed(self):
        print("")
        print("")
        print("\x1b[32mTEST PASSED")
        print("\x1b[0m")

    def remove_null_rows(self, test_frame):
        if test_frame.isnull().any().any() == 0:
            # self._print_test_failed()
            self._print_test_failed("All null rows in entire table are removed. This is not optimal as some rows containg null values may still be usable")

        elif len(test_frame) < 35000:
            # self._print_test_failed()
            self._print_test_failed("Too many rows are removed. This is not optimal as some rows containg null values may still be usable")

        elif test_frame['OriginAimedDepartureTime'].isnull().sum() >= 65890:
            # self._print_test_failed()
            self._print_test_failed(
                "Over 65 000 rows are missing critical route information and should be removed. \nInspect the data with 'frame.head()' and remove relevant columns containing NaN values. columns = ['column_1','column_2','column_3']")

        elif test_frame['RecordedAtTime'].isnull().sum() > 0\
                or test_frame['OriginAimedDepartureTime'].isnull().sum() > 0\
                or test_frame['DestinationAimedArrivalTime'].isnull().sum() > 0:
            self._print_test_failed(
                "You have removed most of NaN values but more cleaning is required: \nThere are still some rows missing crucial information related to the bus schedule and whether the bus is on time or not. HINT: frame['DestinationAimedArrivalTime'].isnull().sum()")

        elif test_frame['Delay'].isnull().sum() > 0:
            # self._print_test_failed()
            self._print_test_failed("You have removed most of NaN values but more cleaning is required: \nFor the machine learning later on, we need to know if a bus is on schedule, ahead or behind. " + str(test_frame['Delay'].isnull().sum()) + " rows are currently missing this information")

        elif test_frame['TripId'].isnull().sum() > 0:
            # self._print_test_failed()
            self._print_test_failed( "You have removed most of NaN values but more cleaning is required: \n " +str(test_frame['TripId'].isnull().sum()) + " rows are missing an identification for its current trip")

        else:
            self._print_test_passed()


    def remove_redundant_columns(self,test_frame):


        if 'Position' in test_frame.columns and 'Longitude' in test_frame.columns and 'Latitude' in test_frame.columns:
            self._print_test_failed("Some columns contain the same information. Keep the columns that are most similar to the other columns.")

        elif 'Position' in test_frame.columns and (not 'Longitude' in test_frame.columns and not 'Latitude' in test_frame.columns):
            self._print_test_failed("Your are almost there. Remove the column 'Position' instead, and keep the columns 'Longitude' and 'Latitude'. These are easier to work with later")

        elif 'Position' in test_frame.columns and ( 'Longitude' in test_frame.columns and not 'Latitude' in test_frame.columns):
            self._print_test_failed("Your are close. You should keep column 'Latitude' and maybe remove another column")
        elif 'Position' in test_frame.columns and (not 'Longitude' in test_frame.columns and 'Latitude' in test_frame.columns):
            self._print_test_failed("Your are close. You should keep column 'Longitude' and maybe remove another column")
        elif not set(self.include).issubset(test_frame):
            self._print_test_failed("Some important columns removed")
        elif not 'Position' in test_frame.columns and  'Longitude' in test_frame.columns and 'Latitude' in test_frame.columns:
            self._print_test_passed()

        else:
            self._print_test_failed("Some columns contain the same information.")

    def remove_outliers_position(self, test_frame):
        outlier_lat = (test_frame['Latitude'] > 60 ).sum() + (test_frame['Latitude'] < 58 ).sum()
        outlier_lon = (test_frame['Longitude'] > 7.3).sum() + (test_frame['Longitude'] < 4.7).sum()

        if outlier_lat > 0 or outlier_lon > 0:
            self._print_test_failed("Some of the buses are outside Rogaland")
        else:
            self._print_test_passed()
            
    def remove_outliers_time(self, test_frame):
        outlier_date = (test_frame['RecordedAtTime'].astype(str).astype('datetime64[ns]') < datetime(2017, 1, 1)).sum()
        outlier_date_future = (test_frame['RecordedAtTime'].astype(str).astype('datetime64[ns]') > datetime(2017, 3, 20)).sum()
        outlier_time = (test_frame['OriginAimedDepartureTime'] > test_frame['RecordedAtTime']).sum()

        if outlier_date > 0:
            self._print_test_failed("Some of the data is recorded before 2017  \nHINT: test_frame['RecordedAtTime'].map(pd.Timestamp.date).unique() to show all dates")
        elif outlier_date_future > 0:
            self._print_test_failed("Some of the data is recorded in the future! Do we need to predict future bus delays when some of the buses are already driving in the future...? \nHINT: test_frame['RecordedAtTime'].map(pd.Timestamp.date).unique() to show all dates")
        elif outlier_time > 0:
            self._print_test_failed("Records before the scheduled departure time is not interesting")

        else:
            self._print_test_passed()

    def remove_outliers_delay(self, test_frame):
        # TODO: add all outlier checks
        outlier_delay = (test_frame['Delay'] < -1000).sum()
        outlier_delay_max = (test_frame['Delay'] > 2000).sum()

        if outlier_delay > 0:
            self._print_test_failed("One bus is " + str(int(abs(test_frame['Delay'].min()) /60)) + " minutes ahead schedule! Make some assumptions about the delay and filter out the ones outside your chosen range. ")
        elif outlier_delay_max > 0:
            self._print_test_failed("One bus is "+str(int(test_frame['Delay'].max() / 60))+" minutes behind schedule! Make some assumptions about the delay and filter out the ones outside your chosen range.")
        else:
            self._print_test_passed()

    def print_stats(self, test_frame):
        print("")

    def _has_columns(self, test_frame, column):
        counter = 0
        for c in column:
            if c in test_frame.columns:
                counter += 1

        return counter

    def remove_columns_with_null_values(self, test_frame):
        null_values = ['Heading', 'IsMonitored']
        remaining = self._has_columns(test_frame, null_values)

        if set(self.include).issubset(test_frame):

            if remaining == 1:
                msg = str(remaining)+"/"+str(len(null_values))+" columns still contain NaN values. \nHint: frame.isnull().any()"
                self._print_test_failed(msg)

            elif remaining > 0:
                msg = str(remaining)+"/"+str(len(null_values))+" columns still contain NaN values."
                self._print_test_failed(msg)
            else:
                self._print_test_passed()
        else:
            self._print_test_failed("Some important columns removed")

    def remove_hard_coded_columns(self, test_frame):
        null_values = ['NextStopVisitNumber', 'VehicleModes']
        remaining = self._has_columns(test_frame, null_values)

        if set(self.include).issubset(test_frame):
            if remaining > 0:
                msg = str(remaining)+"/" + str(
                    len(null_values))+" columns have one hardcoded value.\nHINT: Use 'test_frame['column_1'].value_counts()' to display unique values in column 'column_1'"
                self._print_test_failed(msg)
            else:
                self._print_test_passed()
        else:
            self._print_test_failed("Some important columns removed")


    def remove_duplicate_entries(self, test_frame):
        columns = ['DestinationAimedArrivalTime', 'DistanceBetweenStops', 'Longitude', 'Latitude',
            'OriginAimedDepartureTime',
            'RecordedAtTime', 'TripId']
        num_duplicates = test_frame.duplicated(columns).sum()
        if num_duplicates > 0:
            self._print_test_failed("Not all duplicates are removed")

        elif len(test_frame) < 20000:
            self._print_test_failed("Too many rows removed. Make sure the duplicate removal is not too general")
        else:
            self._print_test_passed()
