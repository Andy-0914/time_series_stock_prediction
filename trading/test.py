from ib_insync import *
import pandas as pd
# util.startLoop()  # uncomment this line when in a notebook

# util.logToConsole('DEBUG')
ib = IB()
ib.connect('localhost', 7496, clientId=2)
stock = Stock("AAPL", "SMART", "USD")


# bars = ib.reqHistoricalData(
#     stock, endDateTime='', durationStr='30 D',
#     barSizeSetting='1 hour', whatToShow='MIDPOINT', useRTH=True)

# # convert to pandas dataframe (pandas needs to be installed):
# df = util.df(bars)
# # print(df)

# market_data = ib.reqMktData(stock, "221", False, False)
# print(market_data)

contract = Forex("EURUSD")
market_data = ib.reqMktData(contract)

# print(bars)

def onPendingTicker(ticker):
    print("pending ticker event received")
    print(ticker)

ib.pendingTickersEvent += onPendingTicker
ib.run()

# order = LimitOrder('BUY', 5, 130)
# order = MarketOrder('BUY', 10)
# trade = ib.placeOrder(stock, order)
# # print(trade)

# def orderFilled(trade, fill):
#     print("order has been filled")
#     print(trade)
#     print(fill)

# trade.filledEvent += orderFilled

# ib.sleep(3)

# for order in ib.orders():
#     print(order)

# for trade in ib.trades():
#     print(trade)

# ib.run()