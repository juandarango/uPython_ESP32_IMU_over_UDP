import socket


'''
Simple stub class to test stuff with in micropython.
'''
class InitTest():
    def __init__(self, a, b):
        self._a = a
        self._b = b
        print("init complete, object initialized")

    def getA(self):
        return self._a

    def getB(self):
        return self._b

    def setA(self, a):
        self._a = a

    def setB(self, b):
        self._b = b

'''
class to test socket connections with
'''
class TestSocket():
    def __init__(self, targetServer, targetPort):
        self._s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._s.sendto("good morning\n", (targetServer, targetPort))

    def sendString(self, string):
        self._s.sendto(string, (targetServer, targetPort))


