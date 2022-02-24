'''
filter objects
'''

class exponentialFilter():
    def __init__(self, alpha, startValue=None):
        self.alpha = alpha
        self.oldValue = startValue if startValue else 0

    def update(self, x):
        self.oldValue = (self.alpha*x) + ((1-self.alpha)*self.oldValue)
        return self.oldValue

    def setAlpha(self, alpha):
        self.alpha = alpha

    def getAlpha(self):
        return self.alpha

class filteredAcceleration():
    def __init__(self, mpu, alpha=0.99, startValue=None):
        self.mpu = mpu
        self.alpha = alpha
        self.rawSensors = [0, 0, 0]
        self.fAx = exponentialFilter(alpha = self.alpha, startValue = startValue)
        self.fAy = exponentialFilter(alpha = self.alpha, startValue = startValue)
        self.fAz = exponentialFilter(alpha = self.alpha, startValue = startValue)

    def getSensors(self):
        self.rawSensors = self.mpu.read_sensors_scaled()
        return [self.fAx.update(self.rawSensors[0]), 
                self.fAy.update(self.rawSensors[1]), 
                self.fAz.update(self.rawSensors[2])]

