import numpy as np


#TODO: IMPLEMENT EXPONENTIAL SMOOTHING MOVING AVERAGE.



class MeanReversion():

    def __init__(self):
        
        pass



    #use Cutler's RSI to not be data length dependent
    def predict(self, data, period, smoothed=False):

        closePrevious = data[0]
        signals = [0]

        #initialise arrays for up and down moving averages
        downArray = []
        downOldestPointer = 0
        upArray = []
        upOldestPointer = 0

        relativeStrengthIndex = 0

        #calculate up/down values for initial period
        for index, dayClose in enumerate(data[1:]):
        
            dayUp = dayClose - closePrevious if dayClose > closePrevious else 0
            dayDown = closePrevious - dayClose if dayClose < closePrevious else 0

            if index == period + 1: #if we have recorded enough values for our initial moving averages, calculate them:

                movingAverageUp = np.mean(upArray)
                movingAverageDown = np.mean(downArray)

            elif index > period: #for each subsequent day, recalculate the moving averages

                movingAverageUp += (dayUp - upArray[upOldestPointer])/period
                #update up array
                upArray[upOldestPointer] = dayUp
                upOldestPointer = (upOldestPointer + 1) % period

                movingAverageDown += (dayDown - downArray[downOldestPointer])/period
                #update down array
                downArray[downOldestPointer] = dayDown
                downOldestPointer = (downOldestPointer + 1) % period

                #calculate relative strength index from relative strength
                relativeStrengthIndex = 100 - (100 / (movingAverageUp / movingAverageDown + 1))

            else: #if still in initial phase:

                upArray.append(dayUp)
                downArray.append(dayDown)

            closePrevious = dayClose

            signals.append(-1) if relativeStrengthIndex > 70 else (signals.append(1) if relativeStrengthIndex < 30 else signals.append(0))
    
        return signals