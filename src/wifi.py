import network
import machine
from machine import Pin
import gc

def setupWiFi (): 
    gc.collect()

    n = network.WLAN(network.STA_IF)
    n.active(True)                      # making sure to put the device in connection mode
    print("current network status: ")
    print(n.ifconfig())

    foundNetwork = False
    if not n.isconnected():
        print("* scanning for networks")
        # scan for BIKBoxMaster
        # scan for network three times. if not found, continue
        for _ in range(3):
            for availableNetwork in n.scan():
                if availableNetwork[0] == str.encode('BIKBoxMaster'):
                    print("* connecting to network BIKBoxMaster")
                    n.active(True)
                    n.connect('BIKBoxMaster', 'BIKBoxMaster')
                    while not n.isconnected():
                        pass
                    print("* current network config: ", n.ifconfig())
                    foundNetwork=True
            if foundNetwork:
                break

    del(foundNetwork)
    gc.collect()
    return n


