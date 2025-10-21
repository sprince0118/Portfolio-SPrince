import dataInterface
from strategies.MovingAverageCrossover import MovingAverageCrossover
from strategies.MeanReversion import MeanReversion

import matplotlib.pyplot as plot

class StrategyTester:

    def __init__(self, stocks, startDate, endDate):

        #initialise database file
        dataInterface.saveToDatabase(dataInterface.downloadData(stocks, startDate, endDate))

        self.data = dataInterface.loadFromDatabase()
        self.stockList = stocks


    
    def runAll(self, startingCapital):

        for stock in self.stockList:

            #get close data
            closeData = dataInterface.loadFromDatabase(f"{stock}_Close").to_numpy()
            #flatten numpy array
            closeData = [i[0] for i in closeData]


            #pass through previous day to each strategy to return signals
            movingAverageAgent = MovingAverageCrossover(shortDuration=50, longDuration=200)
            movingAverageCrossoverSignals = movingAverageAgent.predict(closeData)

            meanReversionAgent = MeanReversion()
            meanReversionSignals = meanReversionAgent.predict(closeData, 14)


            #get open data
            openData = dataInterface.loadFromDatabase(f"{stock}_Open").to_numpy()
            #flatten numpy array
            openData = [i[0] for i in openData]

            #use signals to simulate performance on a portfolio
            mACEquity = self.simulateSignals(movingAverageCrossoverSignals, openData, startingCapital)
            meanReversionEquity = self.simulateSignals(meanReversionSignals, openData, startingCapital)

            fig, (ax1, ax2) = plot.subplots(2)
            ax1.plot(mACEquity)
            ax1.set(xlabel='Days', ylabel='Equity', title=f'Equity curve for Moving Average Crossover, {stock}')
            ax2.plot(meanReversionEquity)
            ax2.set(xlabel='Days', ylabel='Equity', title=f'Equity curve for Mean Reversion, {stock}')

        plot.show()



    def simulateSignals(self, signals, stockData, capital) -> list:

        stocksOwned = 0
        stocksBorrowed = 0
        equityData = []

        for index, dayPrice in enumerate(stockData):

            #check for borrowed/shorted stock and rebuy
            for j in range(stocksBorrowed):
                capital -= dayPrice
                print(f"Shorted stock bought for {dayPrice}")
            stocksBorrowed = 0

            #interpret signals
            if signals[index] == 1: #buy signal

                #print(f"PREBUY: {stocksOwned}, £{capital}")
                
                stocksOwned += capital % dayPrice   #add stocks based on maximum number we can afford
                capital = capital // dayPrice       #set capital to correct level after buying stock

                #print(f"POSTBUY: {stocksOwned}, £{capital}")

            elif signals[index] == 0:   #sell signal

                capital += stocksOwned * dayPrice
                stocksOwned = 0

            elif signals[index] == -1: #short signal:
                #TODO: Make the number of stocks shorted dictated by risk factor
                capital += dayPrice
                stocksBorrowed += 1
                print(f"Shorted stock sold for {dayPrice}")
            
            
            #recalculate equity and add to records
            equityData.append(capital + dayPrice * stocksOwned)

        return equityData

        


classTest = StrategyTester(["GOOG"], "2005-01-01", "2025-01-01")
classTest.runAll(startingCapital=1000)