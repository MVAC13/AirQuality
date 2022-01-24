""" scheduler.py
    Executes main.py every 4 hours
    Required packages:
    - time
    - os
    - apscheduler
"""

import time
import os
from apscheduler.schedulers.background import BackgroundScheduler

# calling the main script
script = os.system("main.py")


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(script, 'interval', hours=4)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # this is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()