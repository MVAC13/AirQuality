""" airquality.py
    Scrapes air quality data.
    Required packages:
    - requests
    - pandas
    - lxml
    - datetime
"""

from datetime import datetime
import lxml.html as lh
import pandas as pd
import requests


def aqtable(url):
    """ Scrapes air quality data table from website """
    # requesting page
    page = requests.get(url)

    # store the content under doc
    doc = lh.fromstring(page.content)

    # parse the date stored between <tr>..</tr>
    tr_elements = doc.xpath('//tr')

    # check the length
    [len(T) for T in tr_elements[:12]]

    # parse table header
    tr_elements = doc.xpath('//tr')

    # create empty list
    col = []
    i = 0

    # storing element for each row
    for t in tr_elements[0]:
        i += 1
        name = t.text_content()
        print('%d:"%s"' % (i, name))
        col.append((name, []))

    # storing data from second row onwards
    for j in range(1, len(tr_elements)):
        # T is our j'th row
        T = tr_elements[j]
        # i is the index of our column
        i = 0
        # iterate through each element of the row
        for t in T.iterchildren():
            data = t.text_content()
            # check if row is empty
            if i > 0:
                # convert any numerical value to integers
                try:
                    data = int(data)
                except:
                    pass
            # append the data to the empty list of the i'th column
            col[i][1].append(data)
            # increment i for the next column
            i += 1

    # checking length
    [len(C) for (title, C) in col]

    # create a data frame
    ddict = {title: column for (title, column) in col}
    df = pd.DataFrame(ddict)

    # removing unnecessary letters from TIMESTAMP column
    df['TIMESTAMP'] = df['TIMESTAMP'].str.replace('\n\t\t\t\t\t', '')
    # change datetime format to d/m/y h:m
    df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'], format="%Y-%m-%d %H:%M")
    df['TIMESTAMP'] = df['TIMESTAMP'].dt.strftime("%d/%m/%Y %H:%M")
    return df


def formatting(df):
    """ split text columns into two columns and changes data type"""
    # setting all floats to 2 digits in general
    pd.options.display.float_format = "{:.2f}".format

    # define all the columns to perform the split
    # could also be an input of the function
    cols = ['NO2', 'SO2', 'O3', 'PM10', 'PM2.5', 'CO', 'TEMP',
            'HUM', 'AIRPRES', 'WS', 'WD', 'NO', 'BENZENE']

    # to get all result columns available
    res_cols = ['TIMESTAMP']
    # iterate over the columns to split
    for col in cols:
        # use try/except instead of if to be able to handle weird columns
        try:
            # add the column to select in the result
            res_cols.append(col)
            # now split the column and expand one time only, in case several space
            df[[col, col + '_UNIT']] = df[col].astype(str).str.split(' ', expand=True, n=1)
            # add the unit column only if the split works
            res_cols.append(col + '_UNIT')
            # in case of the split does not work
        except ValueError:
            print(f'Error for column {col}')
        # from string to float, coerce (aka replace by NaN) if not possible
        df[col] = pd.to_numeric(df[col], downcast="float", errors='coerce')

    # order columns
    df = df[res_cols]
    return df


def aqexport(df, station, path):
    """ Exports data to excel format """
    # getting today's date and time
    now = datetime.now()

    # change date/time format
    dt = now.strftime("%d%m%Y_%H%M%S")
    # file name
    name_df = station + '_' + dt + '.xlsx'

    # exporting to xlsx
    df.to_excel(path + '/' + name_df, index=False)


# air quality stations
# attard
attard = aqtable('https://era.org.mt/air-quality-widget/air-quality-widget-table/?station=624100')
attard[['SO2', 'PM10', 'CO', 'BENZENE']] = 'None'
attard['AIRPRES'].replace(',', '', regex=True, inplace=True)
attard = formatting(attard)
aqexport(attard, 'attard', 'C:\GIS_Projects\Mappa\AirQuality')

# gharb
gharb = aqtable('https://era.org.mt/air-quality-widget/air-quality-widget-table/?station=623100')
gharb[['PM2.5', 'AIRPRES', 'BENZENE']] = 'None'
gharb = formatting(gharb)
aqexport(gharb, 'gharb',
         'C:\GIS_Projects\Mappa\AirQuality')

# msida
msida = aqtable('https://era.org.mt/air-quality-widget/air-quality-widget-table/?station=622100')
msida['AIRPRES'].replace(',', '', regex=True, inplace=True)
msida = formatting(msida)
aqexport(msida, 'msida',
         'C:\GIS_Projects\Mappa\AirQuality')

# zejtun
zejtun = aqtable('https://era.org.mt/air-quality-widget/air-quality-widget-table/?station=570100')
zejtun[['CO', 'BENZENE']] = 'None'
zejtun['AIRPRES'].replace(',', '', regex=True, inplace=True)
zejtun = formatting(zejtun)
aqexport(zejtun, 'zejtun',
         'C:\GIS_Projects\Mappa\AirQuality')

# stpaulsbay
stpaulsbay = aqtable('https://era.org.mt/air-quality-widget/air-quality-widget-table/?station=1180100')
stpaulsbay[['PM10', 'PM2.5']] = 'None'
stpaulsbay['AIRPRES'].replace(',', '', regex=True, inplace=True)
stpaulsbay = formatting(stpaulsbay)
aqexport(stpaulsbay, 'stpaulsbay',
         'C:\GIS_Projects\Mappa\AirQuality')

# senglea
senglea = aqtable('https://era.org.mt/air-quality-widget/air-quality-widget-table/?station=643100')
senglea[['O3', 'BENZENE']] = 'None'
senglea['AIRPRES'].replace(',', '', regex=True, inplace=True)
senglea = formatting(stpaulsbay)
aqexport(senglea, 'senglea',
         'C:\GIS_Projects\Mappa\AirQuality')
