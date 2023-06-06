def help():
    operations = {"Query Algorand ": "q","Generate Graphics ": "g","Generate Report ": "r","Exit App ": "exit"}
    print("This CLI can perform 2 functions.\n"+
          "1 - Query Algorand Network to acquire block and transaction data.\n" + 
          "2 - Generate graphics from stored block/transaction data.\n" + 
          "PLEASE NOTE: This application is only capable of storing 1 instance of data.\n" + 
          "Graphics, and data will be overwritten when a new insatnce is generated\n\n")
    for key, value in operations.items():
        print("{} ----------- '{}'\n".format(key, value))