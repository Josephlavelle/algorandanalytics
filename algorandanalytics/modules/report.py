import pandas as pd
import datetime
def generateReport(path: str):
    #Source data from written csv
    blocks = pd.read_csv(path)

    transactions = blocks.dropna()
    #Calculate overall average TPS
    minTime = min(transactions["timestamp"])
    maxTime = max(transactions["timestamp"])
    transactionCount = len(transactions)
    avgTPS = (maxTime- minTime)/transactionCount

    #Generate Graph of TPS
    plotTPS = transactions.plot.hist(column = ["round-time"])
generateReport("../data/blockTransactions.csv")
    
