import modules.query as q

print("Welcome to Algorand Analyzer! \nThe purpose of this app is to provide insights into the transactions and blocks of the Algorand network.")
print("To continue - Specify a range of blocks by including a start and end integer")
startBlock = input("Starting Block: ")
endBlock = input("Ending Block (inclusive): ")

queryData = q.queryAlgorand(int(startBlock),int(endBlock),["payment-transaction","asset-transfer-transaction"])

queryData.to_csv("data/blockTransactions.csv")
print("Successfully wrote results")
