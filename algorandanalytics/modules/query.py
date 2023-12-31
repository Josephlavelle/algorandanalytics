import requests as req
import pandas as pd
import time

#Functions

def getAuth(file):
    authDict = {}
    try:
        with open(file) as authFile:
            for line in authFile:
                name,var = line.partition(": ")[::2]
                authDict[name.strip()] = str(var.strip())
        return authDict
    except Exception as e:
        raise Exception(f"Invalid Path Exception -> {file} not found")

def isOfInterest(d: dict, ofInterest: list):
    '''
    Checks if dictionary contains a key listed in the ofInterest list
    '''
    for item in ofInterest:
        if d.get(item) != None:
            return True
    return False

def getBlockData(block: int, typesOfInterest: list, key):
    '''
    Gets the transactions for a specific block. If the block has no transactions of the listed types
    of interests it returns a single row with the block info and None in the transaction columns
    '''
    #API INFO
    url = "https://mainnet-algorand.api.purestake.io/idx2//v2/blocks/" + str(block)
    try:
        r = req.get(url = url ,headers =  key)
    except:
        raise Exception(" Error querying API for block {}".format(block))
    
    if r.status_code != 200:
        raise Exception("Error querying API for block {} - Status Code: {}".format(block,r.status_code))

    blockData = r.json()
    transactions = blockData["transactions"]
    transactionsCount = len(transactions)

    if transactionsCount == 0:
        blockDf = pd.DataFrame({"tx-type": [None], "round-time": [None]})
        blockDf["block"] = block
        blockDf["timestamp"] = blockData["timestamp"]
        return blockDf

    blockData["transactions"] = filter(lambda d: isOfInterest(d = d, ofInterest= typesOfInterest), transactions)
    df = pd.DataFrame.from_dict(blockData["transactions"])
    df["block"] = block
    df["timestamp"] = blockData["timestamp"]
    transactionData = df[["tx-type","round-time","block","timestamp"]]
    return transactionData

def queryAlgorand(startBlock: int, endBlock: int, txnTypes: list, authPath: str):
    '''
    Iterates through the range of supplied blocks. Extracts every transaction of type in 'txnTypes'
    and appends to a data frame. Blocks with no transactions of interest are appended with the 'tx-type'
    and 'round-time' columns empty. The data frame is then written to disk in the directory /data
    '''
    authDict = getAuth(authPath)
    key = {"X-API-Key":authDict["algorand"]}
    querySize = endBlock-startBlock + 1
    if querySize < 0:
        raise Exception("startBlock must be bigger than endBlock")
    

    print("Starting Query of " + str(querySize) + " blocks")
    #Initialize Data frame on first query
    currentBlock = startBlock
    blocks = [getBlockData(currentBlock, txnTypes, key)]
    count = 1
    lowTime = time.time()
    totalBlocks = 0
    #Query all blocks in range
    while currentBlock < endBlock:
        #If over 10 queries have been ran in the last second then pause
        if count >= 10:
            totalBlocks += count
            print("Querying Block {}/{}".format(totalBlocks,querySize))
            if time.time() - lowTime < 1000:
                time.sleep(0.1)
            lowTime = time.time()
        currentBlock += 1
        count += 1
        blocks.append(getBlockData(currentBlock, txnTypes, key))
    return pd.concat(blocks)
