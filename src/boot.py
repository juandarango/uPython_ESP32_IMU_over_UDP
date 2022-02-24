import gc
import network

gc.collect()

n = network.WLAN(network.STA_IF)
n.active(True)                      # making sure to put the device in connection mode
print("* BOOT: current network status: ")
print("* BOOT: {}".format(n.ifconfig()))

knownNetworks = {
        "BIKBoxMaster" : "BIKBoxMaster",
        "san-thinkpad" : "BIKBoxMaster",
        }

foundNetwork = False

if not n.isconnected():
    print("* BOOT: scanning for networks")
    # scan for BIKBoxMaster
    # scan for network three times. if not found, continue
    for _ in range(3):
        for availableNetwork in n.scan():
            if availableNetwork[0].decode() in knownNetworks.keys():
                print("* BOOT: connecting to network {}".format(availableNetwork[0].decode()))
                n.active(True)
                n.connect(availableNetwork[0].decode(), knownNetworks[availableNetwork[0].decode()])
                while not n.isconnected():
                    pass
                print("* BOOT: current network config: {}".format(n.ifconfig()))
                foundNetwork=True
        if foundNetwork:
            break

del(foundNetwork)
gc.collect()

