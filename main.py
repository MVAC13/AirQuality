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
