import json
import time
import os

from datetime import datetime
from stockapi import get_historical_data_batched
from setups import analyze_setups
from fundamentals import update_earnings_calendar

BATCH_SIZE = 1
SAMPLE_PERIOD = 30
HISTORICAL_DAYS = 504

#https://www.sec.gov/file/company-tickers
TICKERS_FILE = 'company_tickers.json'

EARNINGS_FILE_NAME = 'earnings_calendar.json'
EARNINGS_FUTURE_DAYS = 30

OUTPUT_FILENAME = f"analysis_result_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.json"

def get_company_tickers():
    with open(TICKERS_FILE, 'r') as file:
        return json.load(file)

def process_batch(batch, earnings_data):
    symbols = []
    titles = {}
    for item in batch:
        symbol = item["ticker"].replace('-', '.')
        symbols.append(symbol)
        titles[symbol] = item["title"]
    try:
        # Get batched historical data
        data = get_historical_data_batched(symbols, HISTORICAL_DAYS)
        for symbol, df in data.items():
            title = titles[symbol]
            print(f'Analyzing [{symbol}] - {title}')
            result = analyze_setups(symbol, df, earnings_data, SAMPLE_PERIOD)
            if result is not None:
                add_json_to_list(result)
    except Exception as e:
        print(f"An error occurred: {e}")
    time.sleep(1.15)

def read_json_list_from_file():
    if os.path.exists(OUTPUT_FILENAME):
        with open(OUTPUT_FILENAME, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                # Return an empty list if the file is empty or contains invalid JSON
                return []
    return []

def write_json_list_to_file(data):
    with open(OUTPUT_FILENAME, 'w') as file:
        json.dump(data, file, indent=4)

def add_json_to_list(new_json):
    # Read the existing list from the file
    json_list = read_json_list_from_file()
    
    # Append the new JSON object
    json_list.append(new_json)
    
    # Write the updated list back to the file
    write_json_list_to_file(json_list)

company_tickers = get_company_tickers()
update_earnings_calendar(EARNINGS_FUTURE_DAYS, EARNINGS_FILE_NAME)
with open(EARNINGS_FILE_NAME, 'r') as json_file:
    earnings_data = json.load(json_file)
    ticker_list = list(company_tickers.values())
    for i in range(0, len(ticker_list), BATCH_SIZE):
        batch = ticker_list[i:i + BATCH_SIZE]
        process_batch(batch, earnings_data)