from ib_insync import *
import pandas as pd
# from PIL import Image

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1)

stock = Stock("AAPL", "SMART", "USD")
ib.qualifyContracts(stock)
# print(stock)

# ib.sleep(1)
chains = ib.reqSecDefOptParams("AAPL", "", stock.secType, stock.conId)

with pd.option_context('display.max_rows', 1000, 'display.max_columns', 1000):
    print(util.df(chains))
