import time
import datetime
import queue
import pandas as pd

# from collections import deque
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.client import Contract
from threading import Thread, Lock
from lightweight_charts import Chart

INITIAL_SYMBOL = "TSM"
INITIAL_TIMEFRAME = "5 mins"

DEFAULT_HOST = '127.0.0.1'
DEFAULT_CLIENT_ID = 1

LIVE_TRADING = False
TRADING_PORT = 7496 if LIVE_TRADING else 7497

data_queue = queue.Queue()
lock = Lock()

class IBClient(EWrapper, EClient):
     
    def __init__(self, host, port, client_id):
        EClient.__init__(self, self) 
        
        self.connect(host, port, client_id)

        thread = Thread(target=self.run)
        thread.start()


    def error(self, req_id, code, msg, misc):
        if code in [2104, 2106, 2158]:
            print(msg)
        else:
            print('Error {}: {}'.format(code, msg))


    def historicalData(self, req_id, bar):
        print(bar)

        t = datetime.datetime.fromtimestamp(int(bar.date))

        # create bar dictionary for each bar received
        data = {
            "date": t,
            "open": bar.open,
            "high": bar.high,
            "low": bar.low,
            "close": bar.close,
            "volume": int(bar.volume)
        }

        print(data)

        # put the data into queue
        data_queue.put(data)


    # callback when all historical data has been received
    def historicalDataEnd(self, reqId, start, end):
        print(f"end of data {start} {end}")

        update_chart()


def get_bar_data(symbol, timeframe):
    print(f"getting bar data for {symbol} {timeframe}")

    contract = Contract()
    contract.symbol = symbol
    contract.secType = 'STK'
    contract.exchange = 'SMART'
    contract.currency = 'USD'
    what_to_show = 'TRADES'

    client.reqHistoricalData(
        2, contract, '', '30 D', timeframe, what_to_show, True, 2, False, []
    )

    time.sleep(1)
       
    chart.watermark(symbol)

def update_chart():
    try:
        bars = []
        while True: # keep checking the queue for new data
            lock.acquire()
            data = data_queue.get_nowait()
            bars.append(data)
            lock.release()
    except queue.Empty:
        print("empty queue!")
    finally:
        # once we have received all the data, convert to pandas dataframe
        df = pd.DataFrame(bars)
        print(df)

        # set the data on the chart
        if not df.empty:
            chart.set(df)

        # once we get the data back, we don't need a spinner anymore
            chart.spinner(False)

# get new bar data when the user changes timeframes
def on_timeframe_selection(chart):
    print("selected timeframe")
    symbol = chart.topbar["symbol"].value,
    timeframe = chart.topbar["timeframe"].value
    print(symbol, timeframe)
    get_bar_data(symbol, timeframe)

#  get new bar data when the user enters a different symbol
def on_search(chart, searched_string):
    get_bar_data(searched_string, chart.topbar["timeframe"].value)
    chart.topbar["symbol"].set(searched_string)



if __name__ == '__main__':
    client = IBClient(DEFAULT_HOST, TRADING_PORT, DEFAULT_CLIENT_ID)
    time.sleep(1)

    chart = Chart(toolbox=True, width=1000, inner_width=0.6, inner_height=1)
    chart.legend(True)
    chart.topbar.textbox('symbol', INITIAL_SYMBOL)
    chart.topbar.switcher('timeframe', ('5 mins', '15 mins', '1 hour'), default='5 mins', func=on_timeframe_selection)

    # set up a function to call when searching for symbol
    chart.events.search += on_search

    get_bar_data(INITIAL_SYMBOL, INITIAL_TIMEFRAME)

    chart.show(block=True)

    # contract = Contract()
    # contract.symbol = INITIAL_SYMBOL
    # contract.secType = 'STK'
    # contract.exchange = 'SMART'
    # contract.currency = 'USD'
    # what_to_show = 'TRADES'

    # client.reqHistoricalData(2, contract, '', '30 D', INITIAL_TIMEFRAME, what_to_show, True, 2, False, [])

    # time.sleep(1)