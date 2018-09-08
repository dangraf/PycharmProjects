from Ticker.data_getters import *
from Ticker.ticker_scheduler import Ticker_Scheduler
from time import sleep


task_5min = Ticker_Scheduler(update_period_s=60 * 5, callback_list=[get_bitcoin_fees,
                                                                    get_coinmarketcap,
                                                                    get_fear_greed_index,
                                                                    get_global_cap],
                             taskname='5min tasks')

task_15min = Ticker_Scheduler(update_period_s=60 * 15, callback_list=[get_news_data,
                                                                      get_bitcoincharts_data],
                              taskname='15min tasks')
task_5min.start_thread()
task_15min.start_thread()
while(1):
    sleep(20)
