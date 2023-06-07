import sys
sys.path.append('..')
import algorandanalytics.modules.io as io
import algorandanalytics.modules.query as q
import algorandanalytics.modules.report as report


def test_queryNoTxns():
    output = q.getBlockData(100,["payment-transaction","asset-transfer-transaction"])
    assert output.iat[0,0] == None 
    assert output.iat[0,1] == None
    assert output.iat[0,2] == 100
    assert output.iat[0,3] == 1560213700

def test_queryTxn():
    output = q.getBlockData(20923000,["payment-transaction","asset-transfer-transaction"])
    print(len(output))
    for i in range(5):
        print(output.iat[1,i])
    assert len(output) == 45
    assert output.iat[1,0] == "axfer"
    assert output.iat[1,1] == 1652205614
    assert output.iat[0,2] == 20923000
    assert output.iat[1,3] == 1652205614
def test_queryNegNum():
    try:
        output = q.getBlockData(-20923000,["payment-transaction","asset-transfer-transaction"])
    except:
        assert True
    else:
        assert 1 == 0
def test_ofInterest():
    interesting = {
        "interesting": 1,
        "notInteresting": 2,
        "interesting2":3
        }
    notInteresting = {
        "notInteresting": 1,
        "alsoNotInteresting": 2,
        "nope":3
        }
    assert q.isOfInterest(interesting, ["interesting"]) == True
    assert q.isOfInterest(notInteresting, ["interesting"]) == False
def test_rangeQuery():
    output = q.queryAlgorand(50000,50010,["payment-transaction","asset-transfer-transaction"])
    assert len(output) == 11
def test_invalidRange():
    try:
        output = q.queryAlgorand(500,400,["payment-transaction","asset-transfer-transaction"])
    except:
        assert True
    else:
        assert 1 == 0
def test_wrongTxnTypes():
    low, high = 7000, 7050
    output = q.queryAlgorand(low,high,["interesting"])
    assert len(output) == high - low + 1
def rightTransactionTypes():
    low, high = 23923000, 23923200
    types = ["payment-transaction","asset-transfer-transaction"]
    output = q.queryAlgorand(low,high,types)
    txnTypes = output["tx-type"].unique().tolist()
    for s in txnTypes:
        assert s in ["axfer","pay"]