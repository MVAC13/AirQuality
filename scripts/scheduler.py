""" scheduler.py
    Executes main.py every 4 hours
    Required packages:
    - time
    - os
"""

import os
import time

while True:
  os.system("python C:\\Users\\Veronica\\PycharmProjects\\AirQuality\\scripts\\main.py")
  time.sleep(240*60)