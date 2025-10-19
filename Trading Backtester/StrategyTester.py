import dataInterface
from strategies.MovingAverageCrossover import MovingAverageCrossover

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
            simAgent = MovingAverageCrossover(shortDuration=50, longDuration=200)
            movingAverageCrossoverSignals = simAgent.predict(closeData)
            #MeanReversion.predict()

            #get open data
            openData = dataInterface.loadFromDatabase(f"{stock}_Open").to_numpy()
            #flatten numpy array
            openData = [i[0] for i in openData]

            #use signals to simulate performance on a portfolio
            mACEquity = self.simulateBasedOnSignals(movingAverageCrossoverSignals, openData, startingCapital)

            

            fig, ax = plot.subplots()
            ax.plot(mACEquity)
            ax.set(xlabel='Days', ylabel='Equity', title=f'Equity curve for Moving Average Crossover, {stock}')

        plot.show()



    def simulateBasedOnSignals(self, signals, stockData, capital) -> list:

        stocksOwned = 0
        equityData = []

        for index, dayPrice in enumerate(stockData):

            #interpret signals
            if signals[index] == 1: #buy signal

                #print(f"PREBUY: {stocksOwned}, £{capital}")
                
                stocksOwned += capital % dayPrice   #add stocks based on maximum number we can afford
                capital = capital // dayPrice       #set capital to correct level after buying stock

                #print(f"POSTBUY: {stocksOwned}, £{capital}")

            else:   #sell signal

                capital += stocksOwned * dayPrice
                stocksOwned = 0
                
            #recalculate equity and add to records
            equityData.append(capital + dayPrice * stocksOwned)

        return equityData

        


classTest = StrategyTester(["GOOG"], "2021-01-01", "2025-01-01")
classTest.runAll(startingCapital=15000)