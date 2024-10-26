# data_fetcher.py
import pandas as pd
from datetime import timezone
from api.binance import Binance, Intervals  
import utils

def fetch_binance_data(symbol, interval, start, end):
    api = Binance({})
    delta = Intervals[interval]
    
    start_ts = int(start.timestamp() * 1000)
    end_ts = int(end.timestamp() * 1000)

    status, data = api.getklines(symbol, interval, 10000, start_ts, end_ts)
    df = utils.klinestodataframe(data)
    ohlc = df

    while data:
        new_start = (ohlc.index[-1] + delta).replace(tzinfo=timezone.utc)
        new_start_ts = int(new_start.timestamp() * 1000)
        
        if new_start >= end:
            break

        status, data = api.getklines(symbol, interval, 10000, new_start_ts, end_ts)
        if data:
            df = utils.klinestodataframe(data)
            ohlc = pd.concat([ohlc, df])

    return ohlc
