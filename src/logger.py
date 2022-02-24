'''
__2019-02-07 Do 13:26__
Logger object 

simple class to handle incomming data and save it to a file on the sd card
'''

import os
import gc
import time

DEBUG_LOGGER = False

class Logger():
    def __init__(self, SD, RTC):
        if not "data" in os.listdir("/"):
            raise Exception("* ERROR: could not find data directory")

        self.sd = SD
        self.RTC = RTC
        self.lastFlush = time.ticks_ms()

        sep = "-"
        ctime = RTC.datetime()
        timestamp = sep.join(map(str, (ctime[0], ctime[1], ctime[2], ctime[4], ctime[5], ctime[6])))
        print("* LOGGER: creating file with timestamp: {}".format(timestamp))
        
        try:
            self.logfile = open("/data/{}.dat".format(timestamp), "w")
        except:
            print("* LOGGER ERROR: could not open filehandle: /data/{}.dat".format(timestamp))
        
        self.logfile_counter = 1
        self.logfile_timestamp = timestamp
        self.logfile.write("# logfile created at {}\n".format(RTC.datetime()))
        self.logfile.write("# timestamp ax ay az temp gx gy gz\n")
        self.logfile.flush()

        del(sep, ctime, timestamp)
        gc.collect()

    def log(self, data):
        # check if logfile still writeable
        # check for current log files size:
        size = self.logfile.tell()
        if size > 6.4e7:            # 64 MB
            self.logfile.flush()
            self.logfile.close()
            try:
                self.logfile = open("/data/{}-{}.dat".format(self.logfile_timestamp, self.logfile_counter), "w")
                self.logfile_counter += 1
            except:
                print("* LOGGER ERROR: could not open filehandle: /data/{}-{}.dat".format(self.logfile_timestamp, self.logfile_timestamp))

        if type(data) == type(str()):
            self.logfile.write("{} {}\n".format("-".join(map(str, self.RTC.datetime())), data))
#             self.logfile.flush()
        elif type(data) == type(list()) or type(data) == type(tuple()):
            self.logfile.write("{} {}\n".format("-".join(map(str, self.RTC.datetime())), " ".join(map(str, data))))
 #            self.logfile.flush()
        elif type(data) == type(dict()):
            print("* LOGGER WARNING: dicts are not supported yet for logging")
        else:
            print("* LOGGER WARNING: unknown date type {}, skipping".format(type(data)))
        
        if time.ticks_ms() - self.lastFlush > 1000:
            if DEBUG_LOGGER: print("* LOGGER: flusing")
            self.logfile.flush()
            self.lastFlush = time.ticks_ms()
#        gc.collect()

    def closeLog(self):
        self.logfile.flush()
        self.logfile.close()
