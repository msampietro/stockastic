## Stock Analysis Project

**Project Structure**

- **stockapi.py**: Contains functions to interface with stock data APIs, such as fetching historical data for a list of stocks (https://twelvedata.com/docs#analysis).
- **indicators.py**: Implements various technical indicators used in the analysis, including RSI (Relative Strength Index), SMA (Simple Moving Average), EMA (Exponential Moving Average), ADX (Average Directional Index), and others.
- **fundamentals.py**: Handles the fetching and updating of fundamental data such as earnings calendars. It ensures that the latest earnings dates are up-to-date for analysis.
- **analyzer.py**: Contains functions and logic for analyzing stock data. It utilizes various technical indicators to identify potential trading setups based on predefined criteria, such as moving averages, RSI, stochastic oscillators, and ADX.
- **setups.py**: Defines different trading setups and strategies based on the technical indicators calculated in _indicators.py_. It provides the logic for determining whether a particular stock meets the criteria for a bullish or bearish setup.
- **main.py**: This is the main script that orchestrates the data fetching, analysis, and results storage. It reads a list of company tickers (https://www.sec.gov/file/company-tickers), fetches their historical data, analyzes them using different setups, and saves the analysis results to a JSON file.
