import json
import os

import pandas as pd

# Settings to display dataframe rows without breaking
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 3000)


def fileNameSortKey(fileName):
    """Return a key string that gives the sort order of the source files."""
    prefix = fileName[0:5]
    year = fileName[11:15]
    moth = fileName[8:10]
    day = fileName[5:7]
    time = fileName[16:]
    return prefix+year+'-'+moth+'-'+day+"_"+time



def getFilenames(pathToBlobs):
    """Retrieve the list of file paths to the source files."""
    fromDir = os.path.join(pathToBlobs)
    if not os.path.exists(fromDir):
        raise AssertionError('Path not found: '+fromDir)
    filenames = os.listdir(fromDir)
    filenames = [os.path.join(fromDir, filename) for filename in filenames if filename.endswith('.txt')]
    filenames = sorted(filenames, key=fileNameSortKey)
    return filenames


def loadData(pathToBlobs):
    """Loads data from disk from a set of jason files. Paramter limitTo tells the loader to abort erlier - after x files."""
    vehicleActivities = []
    print("Reading files from path: ", pathToBlobs)

    fileNames = getFilenames(pathToBlobs)

    numberOfAvailableFiles = len(fileNames)
    print('Reading', numberOfAvailableFiles, 'files from folder '+pathToBlobs)

    for filename in fileNames:
        with open(filename, "rb") as file:
            json_text = json.load(fp=file, encoding='utf-8')
        vehicleActivities.extend(json_text["VehicleActivities"])

    # print(len(vehicleActivities))
    # print(" ")
    return vehicleActivities


def convertColumnTypes(frame):
    """Doing some appropriate datatype conversions."""

    # frame['RecordedAtTime'] = frame['RecordedAtTime'].astype('datetime64[ns]')
    # frame['OriginAimedDepartureTime'] = frame['OriginAimedDepartureTime'].astype('datetime64[ns]')
    # frame['DestinationAimedArrivalTime'] = frame['DestinationAimedArrivalTime'].astype('datetime64[ns]')

    # frame['IsMonitored'] = frame['IsMonitored'].fillna(False)
    # frame['IsMonitored'] = frame['IsMonitored'].astype(bool)
    # frame[['Line', 'From', 'To', 'NextStop', 'TripId', 'LineId', 'OriginStopTerminalCode', 'DestinationTerminalCode',
    #        'NextStopCode', 'TripHeadsign', 'Id']] \
    #     = frame[
    #     ['Line', 'From', 'To', 'NextStop', 'TripId', 'LineId', 'OriginStopTerminalCode', 'DestinationTerminalCode',
    #      'NextStopCode', 'TripHeadsign', 'Id']].astype(unicode)
    # frame['DirectionRef'] = frame['DirectionRef'].astype('category')
    frame['VehicleModes'] = '[1]'  # TODO: hvis liste ikke tomt tar fÃ¸rste element.
    # frame.pop('VehicleModes')
    # frame['VehicleModes'] = frame['VehicleModes'].astype(int)
    return frame


def get_dataframe():
    pathToBlobs = "data/random_one_day"
    dicts = loadData(pathToBlobs)
    frame_1 = pd.DataFrame(dicts)

    frame_2 = convertColumnTypes(frame_1)
    print("Done")
    print("")
    print(" ")

    return frame_2

# if __name__ == '__main__':
#     pathToBlobs = "data/random_one_day"
#     dicts = loadData(pathToBlobs)
#     frame = pd.DataFrame(dicts)
#     cleaner = DataCleaner()
#     frame = cleaner.clean_data(frame)
