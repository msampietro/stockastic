from datetime import datetime, timedelta

BEARISH_TYPE = "BEARISH"
BULLISH_TYPE = "BULLISH"

def check_prices_ma(close_prices, mas_array, days, threshold, type):
    sampled_close_prices = get_sampled_data(close_prices, days)
    if type == BULLISH_TYPE:
        percentage_array = [
            (sampled_close_prices >= get_sampled_data(ma, days)).mean() * 100
            for ma in mas_array
        ]
    elif type == BEARISH_TYPE:
        percentage_array = [
            (sampled_close_prices <= get_sampled_data(ma, days)).mean() * 100
            for ma in mas_array
        ]
    else:
        raise ValueError("Invalid 'type' argument")
    average_percentage = sum(percentage_array) / len(percentage_array)
    return average_percentage >= threshold, average_percentage

def check_rsi_cross(rsi, threshold, type):
    last_rsi = rsi.iloc[-1]
    prev_rsi = rsi.iloc[-2]
    if type == BULLISH_TYPE:
        return (prev_rsi < threshold and last_rsi > threshold), prev_rsi, last_rsi
    elif type == BEARISH_TYPE:
        return (prev_rsi > threshold and last_rsi < threshold), prev_rsi, last_rsi
    else:
        raise ValueError("Invalid 'type' argument")

def check_stochastic_threshold(k, d, threshold, type):
    last_k = k.iloc[-1]
    last_d = d.iloc[-1]
    avg = (last_k + last_d) / 2
    if type == BULLISH_TYPE:
        return avg < threshold, last_k, last_d
    elif type == BEARISH_TYPE:
        return avg > threshold, last_k, last_d
    else:
        raise ValueError("Invalid 'type' argument")

def check_adx_above_threshold(adx, days, adx_threshold, percentage_threshold):
    # Check if ADX has been higher than the threshold most of the time during the period
    sampled_adx = get_sampled_data(adx, days)
    adx_percentage = (sampled_adx >= adx_threshold).mean() * 100
    return adx_percentage >= percentage_threshold, adx_percentage

def check_earnings(symbol, earnings_data):
    for date, earnings_list in earnings_data.items():
        for entry in earnings_list:
            if entry['symbol'] == symbol:
                return date
    return None

def get_sampled_data(data, days):
    date_diff = (datetime.now() - timedelta(days=days)).replace(hour=0, minute=0, second=0, microsecond=0)
    return data.loc[data.index >= date_diff]
