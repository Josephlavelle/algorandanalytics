def help():
    operations = {"Query Algorand ": "q","Generate Graphics ": "g","Exit App ": "exit"}
    print("This CLI can perform 2 functions.\n"+
          "1 - Query Algorand Network to acquire block and transaction data.\n" + 
          "2 - Generate graphics from stored block/transaction data.\n" + 
          "PLEASE NOTE: This application is only capable of storing 1 instance of data.\n" + 
          "Graphics and data will be overwritten when a new insatnce is generated\n\n")
    for key, value in operations.items():
        print("{} ----------- '{}'\n".format(key, value))

def getBlockRange():
        print("Please pick a starting and ending block. It is recommended to have atleast a sample of 100 blocks")
    
        # Collect starting block from user
        startBlock = input("Starting Block: ")
        while not startBlock.isnumeric():
            print("Blocks must be provided as integers")
            startBlock = input("Starting Block: ")

        # Collect ending block from user
        endBlock = input("Ending Block (inclusive): ")
        while not endBlock.isnumeric():
            print("Blocks must be provided as integers")
            endBlock = input("Starting Block: ")

        #Validate input
        while startBlock > endBlock:
            print("Starting block must be lower or equal to end block")

            # Collect starting block from user
            startBlock = input("Starting Block: ")
            while not startBlock.isnumeric():
                print("Blocks must be provided as integers")
                startBlock = input("Starting Block: ")

            # Collect ending block from user
            endBlock = input("Ending Block (inclusive): ")
            while not endBlock.isnumeric():
                print("Blocks must be provided as integers")
                endBlock = input("Starting Block: ")
        return startBlock, endBlock