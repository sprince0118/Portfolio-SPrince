##SCP 6/10/25##

import yfinance as yf
import sqlite3 as sql
import sqlalchemy as sqlAlc
import pandas as pnd

#Return data from YFinance as pandas dataframe. Combines the stock names in the list then downloads and formats the data.
#
#stockList: string[] of stocks to get in form of stock name (ie. ["MSFT", "AAPL"])
#startDate: string start date of range of data in form "YYYY-MM-DD"
#endDate: same as above but for end date of range of data
def downloadData(stockList, startDate=None, endDate=None) -> pnd.DataFrame:

    stocks = ""
    for stock in stockList:
        stocks += f" {stock}"

    data = yf.download(stocks, start=startDate, end=endDate, group_by="ticker")

    #flatten table and combine ticker and price columns (SQL queries do not like tuples)
    newColumns = []
    for col in data.columns:
        newColumns.append(col[0] + "_" + col[1])
    data.columns = newColumns

    return data


#Save data to local database using SQLAlchemy
#
#data: pandas DataFrame to be saved
def saveToDatabase(data) -> None:

    #create database file. could just use SQLite here but Alchemy is better
    engine = sqlAlc.create_engine("sqlite:///stockData.db")

    data.to_sql("StockData", con=engine, if_exists="replace", index=False)


#Loads data from local database as pandas dataframe
#
#column: used to specify columns to return, default all
#command: string SQL command for WHERE condition, default blank
def loadFromDatabase(column="*", condition="") -> pnd.DataFrame:

    engine = sqlAlc.create_engine("sqlite:///stockData.db")
    return pnd.read_sql(f"SELECT {column} FROM StockData {condition}", engine)





#saveToDatabase(downloadData(["MSFT", "AAPL", "GOOG"], "2024-06-09", "2025-06-09"))
#print(loadFromDatabase("AAPL_Close, MSFT_High", "WHERE \"AAPL_Close\" > 200"))
