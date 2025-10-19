import numpy

class MovingAverageCrossover:

    def __init__(self, shortDuration, longDuration):

        self.shortDuration = shortDuration
        self.longDuration = longDuration
        self.signals = []


    def predict(self, data):

        if self.longDuration > len(data):
            print("Warning: Not enough days of past information for moving average to function.")
            return [0] * len(data)
            
        #for the days where the model is gathering data on the initial averages, ensure the signals are 0
        for i in range(self.longDuration):
            self.signals.append(0)

        #store indexes of oldest dates of each moving average for easy calculation of new averages
        shortMAOldest = self.longDuration - self.shortDuration
        longMAOldest = 0

        #calculate initial short- and long-term MAs
        shortMA = numpy.mean(data[shortMAOldest:self.longDuration])
        longMA = numpy.mean(data[:self.longDuration])

        for dayClosePrice in data[self.longDuration:]:

            #interpret signals and add to records
            self.signals.append(1) if (shortMA > longMA) else self.signals.append(0)

            print(f"SHORT: {shortMA}    LONG: {longMA}   BUY: {shortMA > longMA}    DAY PRICE: {dayClosePrice}    SHORT OLDEST: {data[shortMAOldest]}")
            
            #recalculate short and long MAs, then update oldest index
            shortMA += (dayClosePrice - data[shortMAOldest])/self.shortDuration
            longMA += (dayClosePrice - data[longMAOldest])/self.longDuration
            shortMAOldest += 1
            longMAOldest += 1

        return self.signals




