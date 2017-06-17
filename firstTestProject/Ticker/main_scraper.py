import ticker_base as tb
import _thread
from threading import Thread
#OK ./marketcap.p',5.0,'https://api.coinmarketcap.com/v1/ticker/?limit=30
# https://apiv2.bitcoinaverage.com/
# http://bitcoincharts.com/about/markets-api/
# https://blockchain.info/api
# https://bitcoinfees.21.co/api
#https://api.blockchain.info/charts/bitcoin-unlimited-share?timespan=5weeks&rollingAverage=8hours&format=json

#volume comparesio
#median-confirmation-time
#transaction-fees
#cost-per-transaction-percent
#n-unique-addresses
#n-transactions-excluding-popular
#n-transactions-excluding-chains-longer-than-100
t_bitcoin_segwith = tb.ticker_base('./bitcoin_segwith.p',60*60,'https://api.blockchain.info/charts/bip-9-segwit?timespan=1days&format=json')
_thread.start_new_thread( t_bitcoin_segwith.run,() )

t_bitcoin_unlimited = tb.ticker_base('./bitcoin_unlimited.p',60*60,'https://api.blockchain.info/charts/bitcoin-unlimited-share?timespan=1days&format=json')
_thread.start_new_thread( t_bitcoin_unlimited.run,() )

t_bitcoin_fees = tb.ticker_base('./bitcoin_fees.p',60.0,'https://bitcoinfees.21.co/api/v1/fees/recommended')
_thread.start_new_thread( t_bitcoin_fees.run,() )

t_exchange_rates = tb.ticker_base('./exchange_rates.p',60.0,'https://apiv2.bitcoinaverage.com/constants/exchangerates/global')
_thread.start_new_thread( t_exchange_rates.run ,())

t_crypto_coin_market = tb.ticker_base('./crypto_coin_market.p',60.0,'https://api.coinmarketcap.com/v1/ticker/?limit=100')
_thread.start_new_thread( t_crypto_coin_market.run, () )

while 1:
   pass
#thread = Thread(target = t_market.run )
#thread.start()

