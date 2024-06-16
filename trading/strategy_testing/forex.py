from ib_insync import *
import pandas as pd

def onPendingTicker(ticker):
    # print(list(ticker)[0].time)
    ticker = list(ticker)[0]
    print(f"time: {ticker.time} | Bid: {ticker.bid} | Ask: {ticker.ask}", end="\r")

# util.startLoop()
ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1)

contract = Forex("EURUSD")
ib.reqMktData(contract)
ticker = ib.ticker(contract)
# ib.qualifyContracts(ticker)
# print(ticker)

ib.pendingTickersEvent += onPendingTicker

ib.run()