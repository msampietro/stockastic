import warnings
import pandas as pd
import json

from datetime import datetime, timedelta
from twelvedata import TDClient

# https://github.com/twelvedata/twelvedata-python
td = TDClient(apikey="")

def perform_get_historical_data_request(symbol, days):
    with warnings.catch_warnings():
        warnings.simplefilter(action='ignore', category=FutureWarning)
        end_date = datetime.now().strftime('%Y-%m-%d 23:59:59')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d 00:00:00')
        ts = td.time_series(start_date=start_date,
                            end_date=end_date,
                            outputsize=541,
                            symbol=symbol,
                            interval="1day",
                            timezone="America/Argentina/Cordoba",
                            order="asc"
        )
        return ts.as_pandas()

def get_historical_data(symbol, days):
    df = perform_get_historical_data_request(symbol, days)
    #Remove weekends if any
    return df[df.index.dayofweek < 5]

def get_historical_data_batched(symbol_array, days):
        if len(symbol_array) == 1:
             symbol = symbol_array[0]
             df = get_historical_data(symbol, days)
             result = {}
             result[symbol] = df
             return result
        symbols = ",".join(symbol_array)
        df = perform_get_historical_data_request(symbols, days)
        # Convert the 'Date' level of the MultiIndex to a datetime object
        df.index = df.index.set_levels([df.index.levels[0], pd.to_datetime(df.index.levels[1])])
        # Ensure all values are numeric
        for column in df.columns:
            df[column] = pd.to_numeric(df[column], errors='coerce')
       # Remove weekends
        df = df[df.index.get_level_values(1).dayofweek < 5]
        # Group by the first level of the MultiIndex (stock key)
        grouped = df.groupby(level=0)
        # Extract each section and store them in a dictionary
        return {stock_key: group.droplevel(0) for stock_key, group in grouped}

def get_earnings_calendar(start_date, end_date):
    ts = td.get_earnings_calendar(
        start_date=start_date,
        end_date=end_date,
        country='US'
    )
    if ts:
        return ts.as_json()
    return {}
