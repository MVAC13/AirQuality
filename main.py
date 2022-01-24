""" airquality.py
    Scrapes air quality data from ERA.
    Required packages:
    - requests
    - pandas
    - lxml
    - datetime
"""

import schedule
import requests
import pandas as pd
import lxml.html as lh
from datetime import datetime

# creating function to retrieve data
def aqtable(url):
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
    return df


# function to export
def aqexport(df, station, path):
    # removing unnecessary letters from TIMESTAMP column
    df['TIMESTAMP'] = df['TIMESTAMP'].str.replace('\n\t\t\t\t\t', '')

    # getting today's date and time
    now = datetime.now()

    # change date/time format
    dt = now.strftime("%d%m%Y_%H%M%S")

    # file name
    name_df = station + '_' + dt + '.xlsx'

    # exporting to xlsx
    df.to_excel(path + '/' + name_df, index=False)

