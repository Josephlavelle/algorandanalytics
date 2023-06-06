import pandas as pd
import datetime
import matplotlib
import matplotlib.pyplot as plt
def generateFigures(readPath: str, writePath: str):
    #Source data from written csv
    blocks = pd.read_csv(readPath)

    #Get the block interval, tps, and convert epoch to real time data
    tpsData = blocks.groupby(["block","timestamp"]).size().reset_index(name="counts")
    tpsData["blockInterval"] = tpsData["timestamp"].shift(-1) - tpsData["timestamp"]
    tpsData.drop(index=tpsData.index[-1], axis=0, inplace=True)
    tpsData["tps"] = tpsData["counts"]/tpsData["blockInterval"]
    tpsData["time"] = tpsData["timestamp"].transform(lambda x: datetime.datetime.fromtimestamp(x))

    #Calculate overall average TPS
    transactions = blocks.dropna()
    minTime = min(transactions["timestamp"])
    maxTime = max(transactions["timestamp"])
    transactionCount = len(transactions)
    avgTPS = (maxTime- minTime)/transactionCount

    #Generate Transactions per Second Plot and save to output directory
    tpsFig, tpsAx = plt.subplots(figsize=(10,6))
    tpsAx.plot(tpsData["time"],tpsData["tps"])
    tpsAx.set_xlabel('Time (DD HH:mm)')
    tpsAx.set_ylabel('Transactions Per Second')
    tpsAx.set_title('TPS Over Time')
    tpsFig.text(0.5,0.01,"Average is {0:.{1}f} transactions per second".format(avgTPS, 4), ha = "center")
    tpsFig.savefig(writePath + "/TPS.png")
    print("Wrote TPS Figure")

    #Generate Block Interval Time Plot and save to output directory
    blockFig, blockAx = plt.subplots(figsize=(10,6))
    blockAx.scatter(tpsData["time"],tpsData["blockInterval"], s=5)
    blockAx.set_xlabel('Time (DD HH:mm)')
    blockAx.set_ylabel('Block Interval (s)')
    blockAx.set_title('Block Interval Over Time')
    blockFig.savefig(writePath + "/blockInterval.png")
    print("Wrote Block Interval v Time Figure")

    #Generate Zoomed Block Interval Time Plot and save to output directory
    lowerBound, upperBound = minTime,minTime + (maxTime-minTime)/20
    blockFig2, blockAx2 = plt.subplots(figsize=(10,6))
    blockAx2.scatter(tpsData["time"],tpsData["blockInterval"], s=5)
    blockAx2.set_xlabel('Time (DD HH:mm)')
    blockAx2.set_ylabel('Block Interval (s)')
    blockAx2.set_ybound(1.0,7.5)
    blockAx2.set_xbound(datetime.datetime.fromtimestamp(lowerBound),datetime.datetime.fromtimestamp(upperBound))
    blockAx2.set_title('Block Interval Over Time (Zoomed)')
    blockFig2.savefig(writePath + "/blockIntervalZoomed.png")
    print("Wrote Block Interval v Time Figure (Zoomed)")

    #Generate Block Interval vs Transaction Count Plot and save to output directory
    bTFig, bTAx = plt.subplots(figsize=(10,6))
    bTAx.scatter(tpsData["counts"],tpsData["blockInterval"])
    bTAx.set_xlabel("Number of Transactions in Block")
    bTAx.set_ylabel("Block Interval Time (s)")
    bTAx.set_title("Block Interval by Number of Transactions per Block")
    bTFig.savefig(writePath + "/blockTransactions.png")
    print("Wrote Block Interval v Transactions Figure")
    
