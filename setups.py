from indicators import rsi, stochastic, sma, ema, adx, advt
from analyzer import (
    check_prices_ma,
    check_rsi_cross,
    check_stochastic_threshold,
    check_adx_above_threshold,
    check_earnings,
    BULLISH_TYPE,
    BEARISH_TYPE,
)

CONFIG = {
    'SMA_LENGTHS': [50, 100, 200],
    'SMA_PERCENTAGE': 100,
    'EMA_LENGTHS': [8, 21, 34, 55],
    'EMA_PERCENTAGE': 75,
    'STOCH_K': 8,
    'STOCH_D': 3,
    'STOCH_BULLISH_THRESHOLD': 40,
    'STOCH_BEARISH_THRESHOLD': 60,
    'RSI_LENGTH': 2,
    'RSI_BULLISH_THRESHOLD': 10,
    'RSI_BEARISH_THRESHOLD': 90,
    'ADX_LENGTH': 13,
    'ADX_THRESHOLD': 20,
    'ADX_PERCENTAGE': 75,
    'ADTV_THRESHOLD': 1000000,
    'PRICE_THRESHOLD': 5
}

def analyze_setups(symbol, stock_data, earnings_data, period):
    adtv = advt(stock_data)
    close_prices = stock_data['close']
    last_close = close_prices.iloc[-1]

    if adtv < CONFIG['ADTV_THRESHOLD'] or last_close < CONFIG['PRICE_THRESHOLD']:
        return None

    smas = sma(stock_data, CONFIG['SMA_LENGTHS'])
    smas_last_values = {str(length): smas[idx].iloc[-1] for idx, length in enumerate(CONFIG['SMA_LENGTHS'])}
    emas = ema(stock_data, CONFIG['EMA_LENGTHS'])
    emas_last_values = {str(length): emas[idx].iloc[-1] for idx, length in enumerate(CONFIG['EMA_LENGTHS'])}

    stoch = stochastic(stock_data, CONFIG['STOCH_K'], CONFIG['STOCH_D'])
    rsival = rsi(stock_data, CONFIG['RSI_LENGTH'])
    adxval = adx(stock_data, CONFIG['ADX_LENGTH'])
    earnings_date = check_earnings(symbol, earnings_data)

    response = {
        "symbol": symbol,
        "adtv": adtv,
        "close": last_close,
        "earnings_date": earnings_date,
        "smas": smas_last_values,
        "emas": emas_last_values
    }

    for analysis_type in (BULLISH_TYPE, BEARISH_TYPE):
        result = analyze(analysis_type, close_prices, period, smas, emas, rsival, stoch, adxval)
        if result:
            response.update(result)
            return response

    return None

def analyze(analysis_type, close_prices, period, smas, emas, rsi, stoch, adx):
    rsi_threshold = CONFIG['RSI_BULLISH_THRESHOLD'] if analysis_type == BULLISH_TYPE else CONFIG['RSI_BEARISH_THRESHOLD']
    stoch_threshold = CONFIG['STOCH_BULLISH_THRESHOLD'] if analysis_type == BULLISH_TYPE else CONFIG['STOCH_BEARISH_THRESHOLD']

    adx_indicator, adx_percentage = check_adx_above_threshold(adx, period, CONFIG['ADX_THRESHOLD'], CONFIG['ADX_PERCENTAGE'])
    smas_indicator, smas_average_percentage = check_prices_ma(close_prices, smas, period, CONFIG['SMA_PERCENTAGE'], analysis_type)
    emas_indicator, emas_average_percentage = check_prices_ma(close_prices, emas, period, CONFIG['EMA_PERCENTAGE'], analysis_type)
    stoch_indicator, last_k, last_d = check_stochastic_threshold(stoch[0], stoch[1], stoch_threshold, analysis_type)
    rsi_indicator, prev_rsi, last_rsi = check_rsi_cross(rsi, rsi_threshold, analysis_type)

    if all([adx_indicator, smas_indicator, emas_indicator, stoch_indicator, rsi_indicator]):
        return build_result_object(analysis_type, adx_percentage, smas_average_percentage, emas_average_percentage, last_k, last_d, prev_rsi, last_rsi)
    
    return None

def build_result_object(analysis_type, adx_percentage, smas_average_percentage, emas_average_percentage, last_k, last_d, prev_rsi, last_rsi):
    return {
        "type": analysis_type,
        "adx": {
            "threshold": CONFIG['ADX_THRESHOLD'],
            "length": CONFIG['ADX_LENGTH'],
            "percentage": adx_percentage
        },
        "smas": {
            "percentage": smas_average_percentage
        },
        "emas": {
            "percentage": emas_average_percentage
        },
        "stochastic": {
            "k": CONFIG['STOCH_K'],
            "d": CONFIG['STOCH_D'],
            "last_k": last_k,
            "last_d": last_d
        },
        "rsi": {
            "length": CONFIG['RSI_LENGTH'],
            "prev": prev_rsi,
            "last": last_rsi
        }
    }