# Algorand Analyzer

This a basic CLI tool to query the Algorand network for block/transaction data and generate some choice visualizations to help understand some of Algorand's KPIs.

## Description
This app interfaces with the Algorand V2 Indexer using the v2/blocks/{round-number} end point to query data.

When app.py is run, the user will be greeted with a CLI that will them through the 2 main functions of the app -
1. To query block and transaction data from Algorand. 
2. To generate some basic visualizations to help understand core Algorand KPIs
The user will select a range of blocks to query from Algorand, the data will be ingested by the script and written out to a CSV. The block number, genesis hash, and timestamp are stored alongside the transactions of type 'payment-transaction' or 'asset-transfer-transaction'. Due to the nature of the KPIs that are visualized in the second step, the data is stored with each transaction being stored as a row, with each row also containing the containing blocks information. This structure makes it more efficient to transform the data and generate the required plots.

## Usage
To get started. The user must have poetry installed on their system. Once the repo is cloned, running
```
    poetry install
    poetry env use python3
```
will install the dependencies and initialize the environment. Then to start the application, run
```
    poetry run python app.py
```
This will start the CLI. At any point while using the CLI, enter 'help' to be provided with the short list of commands that the app accepts as inputs. The CLI only has 2 real commands - "q" for query and "g" for graphics. "q" will allow the user to submit a new range of blocks to query. Once supplied - the app will run the query against the Algorand Indexer and overwrite the currently stored data. Once the query is finished, the user can then run the "g" command to generate 4 graphics that display KPIs of the algorand network. The app will read in the data from the query, run multiple transformations on it and generate the graphics (overwriting previously stored ones).

Once finished, the user can enter "exit" into the CLI to close the app.

Tests for functions are included in the Tests folder and can be run by calling
```
poetry run pyTest
```
once the environment has been activated.

## Report
A report on my own findings from using this tool can also be found in the report directory.

## Authors
Joseph Lavelle
Joseph.Lavelle@queensu.ca
