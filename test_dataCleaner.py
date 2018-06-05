#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime


class TestDataCleaner:
    include = ['RecordedAtTime', 'OriginAimedDepartureTime', 'DestinationAimedArrivalTime', 'NextStop', 'Delay', 'PercentageBetweenStops', 'DestinationAimedArrivalTime',
        'DistanceBetweenStops', 'Longitude', 'Latitude',
        'OriginAimedDepartureTime',
        'RecordedAtTime', 'TripId']

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
            self._print_test_failed("All null rows in entire table are removed. This is not optimal as some rows containg null values may still be usuable")

        elif len(test_frame) < 35000:
            # self._print_test_failed()
            self._print_test_failed("Too many rows are removed. This is not optimal as some rows containg null values may still be usuable")

        elif test_frame['OriginAimedDepartureTime'].isnull().sum() >= 65890:
            # self._print_test_failed()
            self._print_test_failed(
                "Over 65 000 rows are missing critical route information and should be removed."
                " \nInspect the data with 'frame.head()' and add columns contaning NaN values. columns = ['column_1','column_2','column_3']")

        elif test_frame['RecordedAtTime'].isnull().sum() > 0\
                or test_frame['OriginAimedDepartureTime'].isnull().sum() > 0\
                or test_frame['DestinationAimedArrivalTime'].isnull().sum() > 0:
            self._print_test_failed(
                "There are still some rows missing crucial information related to the bus schedule and whether the bus is on time or not. HINT: frame['DestinationAimedArrivalTime'].isnull().sum()")

        elif test_frame['Delay'].isnull().sum() > 0:
            # self._print_test_failed()
            self._print_test_failed("For the machine learning later on, we need to know if a bus is on schedule, ahead or behind.", test_frame['TripId'].isnull().sum(),
                                    "rows are currently missing this information")

        elif test_frame['TripId'].isnull().sum() > 0:
            # self._print_test_failed()
            self._print_test_failed(test_frame['TripId'].isnull().sum(), "rows are missing an identification for its current trip")

        else:
            self._print_test_passed()

    def remove_outliers(self, test_frame):
        # TODO: add all outlier checks
        outlier_date = (test_frame['RecordedAtTime'].astype(str).astype('datetime64[ns]') < datetime(2017, 1, 1)).sum()
        outlier_lat = (test_frame['Latitude'] > 61).sum()
        outlier_lon = (test_frame['Longitude'] > 7.3).sum()
        outlier_delay = (test_frame['Delay'] < -3000).sum()
        outlier_delay_max = (test_frame['Delay'] > 3000).sum()
        outlier_distance = (test_frame['DistanceBetweenStops'] == 0).sum()
        outlier_time = (test_frame['OriginAimedDepartureTime'] >= test_frame['RecordedAtTime']).sum()

        if outlier_date > 0:
            return False, "Data from more than one day included, revise remove_outliers rule"
        elif outlier_lat > 0:
            return False, "Latitude is outside Rogaland, revise remove_outliers rule"
        elif outlier_lon > 0:
            return False, "Longitude is outside Rogaland, revise remove_outliers rule"
        elif outlier_delay > 0:
            return False, "Buses are way ahead of their schedule, revise remove_outliers rule"
        elif outlier_delay_max > 0:
            return False, "Buses are too delayed, engine malfunction perhaps? revise remove_outliers rule"
        elif outlier_distance > 0:
            return False, "There should be a minimum distance between two stops, right? revise remove_outliers rule"
        elif outlier_time > 0:
            return False, "Records before the departure time from the first stop is not interesting, revise remove_outliers rule"
        else:
            return True, ""

    def print_stats(self, test_frame):
        print("")

    def _has_columns(self, test_frame, column):
        counter = 0
        for c in column:
            if c in test_frame.columns:
                counter += 1

        return counter

    def remove_columns_with_null_values(self, test_frame):

        null_values = ['Heading', 'IsMonitored', 'TripHeadsign']
        remaining = self._has_columns(test_frame, null_values)

        if set(self.include).issubset(test_frame):
            if remaining > 0:
                # print("TEST FAILED:")
                msg = str(remaining)+"/"+str(len(null_values))+" columns still contain NaN values. Hint: frame.isnull().any()"
                self._print_test_failed(msg)
            else:
                # print("TEST PASSED")
                self._print_test_passed()
                # return True, ""
        else:
            # print("TEST FAILED:")
            self._print_test_failed("Some important columns removed")
            # return False, "Some important columns removed"

    def remove_hard_coded_columns(self, test_frame):

        null_values = ['NextStopVisitNumber', 'VehicleModes']
        remaining = self._has_columns(test_frame, null_values)

        if set(self.include).issubset(test_frame):
            if remaining > 0:
                # print("TEST FAILED:")
                msg = str(remaining)+"/", str(
                    len(null_values))+" columns have one hardcoded value. \nHint: Use 'frame['column_1'].value_counts()' to display unique values in column 'column_1'"
                self._print_test_failed(msg)
            else:
                # print("TEST PASSED")
                self._print_test_passed()
                # return True, ""
        else:
            # print("TEST FAILED:")
            self._print_test_failed("Some important columns removed")
            # return False, "Some important columns removed"

    def remove_unwanted_columns(self, test_frame):
        # TODO: Check which columns should be in exclude and include
        exclude = ['VehicleModes', 'NextStopVisitNumber', 'Position',
            'From', 'To', 'PercentageBetweenStops', 'DirectionRef',
            'Heading', 'IsMonitored', 'TripHeadsign']

        include = ['RecordedAtTime', 'OriginAimedDepartureTime', 'DestinationAimedArrivalTime', 'NextStop', 'Delay', 'PercentageBetweenStops', 'DestinationAimedArrivalTime',
            'DistanceBetweenStops', 'Longitude', 'Latitude',
            'OriginAimedDepartureTime',
            'RecordedAtTime', 'TripId']

        null_values = ['Heading', 'IsMonitored', 'TripHeadsign']

        if set(include).issubset(test_frame):
            if set(null_values).issubset(test_frame):
                _
            if set(exclude).issubset(test_frame):
                return False, "You could remove some more columns, revise remove_unwanted_columns rule"
            else:
                return True, ""
        else:
            return False, "Some important columns removed, revise remove_unwanted_columns rule"

    def remove_duplicate_entries(self, test_frame):
        # TODO: check which columns need to be combined for duplicates check
        columns = ['DestinationAimedArrivalTime', 'DistanceBetweenStops', 'Longitude', 'Latitude',
            'OriginAimedDepartureTime',
            'RecordedAtTime', 'TripId']
        num_duplicates = test_frame.duplicated(columns).sum()
        if num_duplicates > 0:
            # print("TEST FAILED:")
            self._print_test_failed("Not all duplicates are removed")
            # return False, "Not all duplicates removed, revise remove_duplicate_entries rule"

        elif len(test_frame) < 20000:
            # print("TEST FAILED:")
            self._print_test_failed("Too many rows removed. Make sure the duplicate removal is not too general")
        else:
            self._print_test_passed()
            # print("TEST PASSED")
            # return True, ""
