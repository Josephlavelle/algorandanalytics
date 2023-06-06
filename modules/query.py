import requests as req
import pandas as pd
import time


#Functions

def isOfInterest(d: dict, ofInterest: list):
    '''
    Checks if dictionary contains a key of interest
    '''
    for item in ofInterest:
        if d.get(item) != None:
            return True
    return False

def getBlockData(block: int, typesOfInterest: list):
    '''
    Gets the transactions for a specific block. If the block has no transactions of the listed types
    of interests it returns a single row with the block info and None in the transaction columns
    '''
    #API INFO
    url = "https://mainnet-algorand.api.purestake.io/idx2//v2/blocks/" + str(block)
    key = {"X-API-Key":"8bIrGK8Wrm8r54ngNWgAI4ECnaZQNZ1x1km9YVQb"}

    r = req.get(url = url ,headers =  key)
    if r.status_code != 200:
        raise Exception("Error Querying API - Status Code: " + str(r.status_code))

    blockData = r.json()
    transactions = blockData["transactions"]
    transactionsCount = len(transactions)

    if transactionsCount == 0:
        blockDf = pd.DataFrame({"tx-type": [None], "round-time": [None]})
        blockDf["block"] = block
        blockDf["timestamp"] = blockData["timestamp"]
        blockDf["genesis-hash"] = blockData["genesis-hash"]
        return blockDf

    blockData["transactions"] = filter(lambda d: isOfInterest(d = d, ofInterest= typesOfInterest), transactions)
    df = pd.DataFrame.from_dict(blockData["transactions"])

    

    
    df["block"] = block
    df["timestamp"] = blockData["timestamp"]
    df["genesis-hash"] = blockData["genesis-hash"]
    transactionData = df[["block","timestamp","genesis-hash","tx-type","round-time"]]
    return transactionData

def queryAlgorand(startBlock: int, endBlock: int, txnTypes: list):
    querySize = endBlock-startBlock
    print("Starting Query of " + str(querySize) + " blocks")
    #Initialize Data frame on first query
    currentBlock = startBlock
    blocks = [getBlockData(currentBlock, txnTypes)]
    count = 1
    lowTime = time.time()
    #Query all blocks in range
    while currentBlock < endBlock:
        #If over 10 queries have been ran in the last second then pause
        if count >= 10:
            print("Querying Block " + str(currentBlock - startBlock) + "/" + str(querySize))
            if lowTime - time.time() < 1000:
                time.sleep(0.1)
            count = 1
            currentBlock += 1
            blocks.append(getBlockData(currentBlock, txnTypes))
            lowTime = time.time()
        currentBlock += 1
        count += 1
        blocks.append(getBlockData(currentBlock, txnTypes))
    return pd.concat(blocks)

res = queryAlgorand(20922999, 20923004, ["payment-transaction", "asset-transfer-transaction"])