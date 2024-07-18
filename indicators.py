import pandas_ta as ta

def sma(data_frame, length_array):
    results = []
    for length in length_array:
        results.append(data_frame.ta.sma(length=length))
    return results

def ema(data_frame, length_array):
    results = []
    for length in length_array:
        results.append(data_frame.ta.ema(length=length))
    return results

def rsi(data_frame, length):
    return data_frame.ta.rsi(length=length)

def stochastic(data_frame, k, d):
    stoch_k_d = []
    stoch_data = data_frame.ta.stoch(k=k, d=d)
    stoch_k_d.append(stoch_data[f'STOCHk_{k}_{d}_{d}'])
    stoch_k_d.append(stoch_data[f'STOCHd_{k}_{d}_{d}'])
    return stoch_k_d

def adx(data_frame, length):
    adx_data = data_frame.ta.adx(length=length)
    return adx_data[f'ADX_{length}']

def advt(data_frame):
    return data_frame['volume'].mean()

def legacy_rsi(close_price_data, length):
    delta = close_price_data.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.ewm(alpha=1/length, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/length, adjust=False).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi