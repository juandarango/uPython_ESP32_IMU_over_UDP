import time
import os
import socket
from machine import I2C, Pin, RTC, SPI, UART

import mpu6050
import micropython
import filters
import fusion

micropython.alloc_emergency_exception_buf(100)

DEBUG = True

if n.isconnected():
    targetIP = n.ifconfig()[2]
else:
    targetIP = '10.42.0.1'
targetPort = 52002

print("* MAIN: current targetIP: {}:{}".format(targetIP, targetPort))

i2c = None
mpu = None
fuse = None

# create an i2c object for the real time clock and the imu
print("* MAIN: creating I2C interface")
try:
    i2c = I2C(scl=Pin(5), sda=Pin(4))
except:
    print("* MAIN ERROR: failed to create i2c interface!")

### MPU ###
# object for the inertial measurement unit
print("* MAIN: creating mpu object")
try:
    mpu = mpu6050.MPU(i2c = i2c, address = 104)
except:
    print("* MAIN ERROR: failed to create mpu object")

try:
    mpu.calibrate()
except:
    print("* MAIN ERROR: failed to calibrate MPU")

# set the low pass filter
# print("* MAIN: setting MPU DLPF to 5 Hz")
# mpu.set_dhpf_mode(4) # -> corresponds to a cut off frequency of 21 Hz (acc) and 20 Hz (gyro)

### UDP Socket ###
print("* MAIN: creating UDP socket to send data")
# create an udp socket to send data to
if n.isconnected():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except:
        print("* MAIN ERROR: failed to create udp socket")
        sock = None
else:
    sock = None
    print("* MAIN WARNING: no network available")

# create fusion object
print("* MAIN: creating fusion filter")
try:
    fuse = fusion.Fusion()
except:
    print("* MAIN ERROR: could not create fusion object")

def logData(mpu, fuse, sock):
    sensorData = ""
    orientationData = ""
    fuseData = ""

    while True:

        cycleTime = time.ticks_ms() # to measure cycle time

        if mpu:
            sensorData = mpu.read_sensors_scaled()
            orientationData = mpu.attitude()
        else:
            sensorData = ""
            orientationData = ""

        if fuse and len(sensorData) > 0:
            fuse.update_nomag(sensorData[0:3], sensorData[4:7])
            fuseData = [fuse.roll,fuse.pitch,fuse.heading,fuse.q]

        if n.isconnected():
            if sock: 
                # sock.sendto("{};;;;".format(str(sensorData)))
                sock.sendto("{};{};{}".format(
                                            str(sensorData),
                                            str(orientationData),
                                            str(fuseData),
                                            ), (targetIP, targetPort))
            # create new socket here?
        else:
            if n.active():
                print("* MAIN ERROR: network no longer available, turning off network")
                n.active(False)
                sock = None

        gc.collect()
        now = time.ticks_ms()
        if DEBUG: print("* MAIN: Current cycle time {} -> f = {}".format((now - cycleTime), 1/((now - cycleTime)/1000)))
        # while (time.ticks_ms() - cycleTime) < 20:
        #     time.sleep_ms(1)

#### start logging function
print("* MAIN: ready")
print("* MAIN: starting measurement")

# for future reference: hard-reset the board if it crashes too often
logCounter = 0
while logCounter < 3:
    try:
        logData(mpu, fuse, sock)
    except:
        print("* MAIN ERROR: logging crashed, restarting")
        logCounter += 1

