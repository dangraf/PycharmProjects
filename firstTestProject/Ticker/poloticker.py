import websocket
import _thread
import time
import json
import ast
import datetime
# bra sida för polonix api http://cryptocurrenciesstocks.readthedocs.io/poloniex.html
# returnerar alla id för alla valutor
# https://poloniex.com/public?command=returnCurrencies

myList= []
def on_message(ws, message):
    if len(message) > 20:
        raw_data = ast.literal_eval(message[11:-1])
        data = [float(i) for i in raw_data[0:6]]
        data.append(datetime.datetime.u)
        myList.append(data[])
        print(data)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("ONOPEN")
    def run(*args):
        # 1001: trollbox (same as heartbeat)
        # 1002: ticker
        # 1003: basecoin
        # 1010: heartbeat
        # ws.send(json.dumps({'command': 'subscribe', 'channel': 1001}))
        ws.send(json.dumps({'command': 'subscribe', 'channel': 1002}))
        # ws.send(json.dumps({'command': 'subscribe', 'channel': 1003}))
        # ws.send(json.dumps({'command': 'subscribe', 'channel': 'BTC_XMR'}))
        while True:
            time.sleep(1)
        ws.close()
        print("thread terminating...")
    _thread.start_new_thread(run, ())

labels = ['currencyPair_id', 'last', 'lowestAsk', 'highestBid', 'percentChange', 'baseVolume',
          'quoteVolume', 'isFrozen', '24hrHigh', '24hrLow']
if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://api2.poloniex.com/",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()