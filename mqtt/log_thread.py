import threading
import time
from datetime import datetime

import pandas as pd


class LogThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name, self.columns = name, ["Time", "Operation", "ID", "Value"]
        self.dfLog = pd.DataFrame(columns=self.columns)

    def log(self, msg):
        print("{} @ {}: {}".format(self.name, time.ctime(time.time()).split(" ")[3], msg))
    def errorLog(self, err):
        print("ERROR: {} @ {}: {}".format(self.name, time.ctime(time.time()).split(" ")[3], err))

    def logExcel(self, operation, id, value):
        self.dfLog = self.dfLog.append([[datetime.today(), operation, id, value]])
        self.dfLog.to_csv("{}.csv".format(self.name))