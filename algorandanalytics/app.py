import modules.query as q
import modules.report as report
import modules.io as io
from os.path import exists
print("Welcome to Algorand Analyzer! \nThe purpose of this app is to provide insights into the transactions and blocks of the Algorand network.")
print("To continue - Specify a range of blocks by including a start and end integer")

command = ""
while command != "exit":
    # Gather User input
    command = input("Welcome to the Main Menu. Enter 'help' for a list of commands\n")
    print("\n")

    #Help
    if command == "help":
        io.help()

    #Query
    elif command == "q":
        #Confirm that user wants to overwrite data
        if exists("./data/blockTransactions.csv"):
            command = input("You will overwrite the currently stored data. Enter 'ok' to confirm\n")
            if command != "ok":
                print("Returning to main menu")
                continue
        
        #Get blocks from user
        startBlock, endBlock = io.getBlockRange()

        print("Starting Query")
        queryData = q.queryAlgorand(int(startBlock),int(endBlock),["payment-transaction","asset-transfer-transaction"], "apiKeys.txt")
        print("Writing Results")
        queryData.to_csv("data/blockTransactions.csv")
        print("Successfully wrote results\n")

    #Graphics
    elif command == "g":
        #Generate Graphics
        print("Generating graphics")
        report.generateFigures("data/blockTransactions.csv","data/images")
        print("Successfully generated all graphics in the ./data/images directory\n")


print("Exiting Application...\n")