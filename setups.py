from indicators import rsi, stochastic, sma, ema, adx, advt
from analyzer import check_prices_ma, check_rsi_cross, check_stochastic_threshold, check_adx_above_threshold, check_earnings

SMA_LENGHTS = [50, 100, 200]
SMA_PERCENTAGE = 100
EMA_LENGHTS = [8, 21, 34, 55]
EMA_PERCENTAGE = 75

STOCH_K = 8
STOCH_D = 3
STOCH_BULLISH_THRESHOLD = 40
STOCH_BEARISH_THRESHOLD = 60

RSI_LENGTH = 2
RSI_BULLISH_THRESHOLD = 10
RSI_BEARISH_THRESHOLD = 90

ADX_LENGTH = 13
ADX_THRESHOLD = 20
ADX_PERCENTAGE = 75

ADTV_THRESHOLD = 1000000
PRICE_THRESHOLD = 5

def analyze_setups(symbol, stock_data, earnings_data, period):
    adtv = advt(stock_data)
    close_prices = stock_data['close']
    last_close = close_prices.iloc[-1]
    if adtv < ADTV_THRESHOLD or last_close < PRICE_THRESHOLD:
        return None
    smas = sma(stock_data, SMA_LENGHTS)
    emas = ema(stock_data, EMA_LENGHTS)
    stoch = stochastic(stock_data, STOCH_K, STOCH_D)
    rsival = rsi(stock_data, RSI_LENGTH)
    adxval = adx(stock_data, ADX_LENGTH)
    earnings_date = check_earnings(symbol, earnings_data)
    result = {
        "symbol": symbol,
        "adtv": adtv,
        "close": last_close,
        "earnings_date": earnings_date
    }
    bullish_result = analyze_bullish(close_prices, period, smas, emas, rsival, stoch, adxval)
    if bullish_result is not None:
        result.update(bullish_result)
        return result
    else:
        bearish_result = analyze_bearish(close_prices, period, smas, emas, rsival, stoch, adxval)
        if bearish_result is not None:
            result.update(bearish_result)
            return result
    return None
        
def analyze_bullish(close_prices, period, smas, emas, rsi, stoch, adx):
    adx_indicator, adx_percentage = check_adx_above_threshold(adx, period, ADX_THRESHOLD, ADX_PERCENTAGE)
    smas_indicator, smas_average_percentage = check_prices_ma(close_prices, smas, period, SMA_PERCENTAGE)
    emas_indicator, emas_average_percentage = check_prices_ma(close_prices, emas, period, EMA_PERCENTAGE)
    stoch_indicator, last_k, last_d = check_stochastic_threshold(stoch[0], stoch[1], STOCH_BULLISH_THRESHOLD)
    rsi_indicator, prev_rsi, last_rsi = check_rsi_cross(rsi, RSI_BULLISH_THRESHOLD)
    if adx_indicator and smas_indicator and emas_indicator and stoch_indicator and rsi_indicator:
        return build_result_object("BULLISH", adx_percentage, smas_average_percentage, emas_average_percentage, last_k, last_d, prev_rsi, last_rsi)
    return None

def analyze_bearish(close_prices, period, smas, emas, rsi, stoch, adx):
    adx_indicator, adx_percentage = check_adx_above_threshold(adx, period, ADX_THRESHOLD, ADX_PERCENTAGE)
    smas_indicator, smas_average_percentage = check_prices_ma(close_prices, smas, period, SMA_PERCENTAGE, 'below')
    emas_indicator, emas_average_percentage = check_prices_ma(close_prices, emas, period, EMA_PERCENTAGE, 'below')
    stoch_indicator, last_k, last_d = check_stochastic_threshold(stoch[0], stoch[1], STOCH_BEARISH_THRESHOLD, 'above')
    rsi_indicator, prev_rsi, last_rsi = check_rsi_cross(rsi, RSI_BEARISH_THRESHOLD, 'below')
    if adx_indicator and smas_indicator and emas_indicator and stoch_indicator and rsi_indicator:
        return build_result_object("BEARISH", adx_percentage, smas_average_percentage, emas_average_percentage, last_k, last_d, prev_rsi, last_rsi)
    return None

def build_result_object(type, adx_percentage, smas_average_percentage, emas_average_percentage, last_k, last_d, prev_rsi, last_rsi):
    return {
            "type": type,
            "adx": {
                "threshold": ADX_THRESHOLD,
                "length": ADX_LENGTH,
                "percentage": adx_percentage

            },
            "smas": {
                "length": SMA_LENGHTS,
                "percentage": smas_average_percentage
            },
            "emas": {
                "length": EMA_LENGHTS,
                "percentage": emas_average_percentage
            },
            "stochastic": {
                "k": STOCH_K,
                "d": STOCH_D,
                "last_k": last_k,
                "last_d": last_d
            },
            "rsi": {
                "length": RSI_LENGTH,
                "prev": prev_rsi,
                "last": last_rsi
            }
        }
