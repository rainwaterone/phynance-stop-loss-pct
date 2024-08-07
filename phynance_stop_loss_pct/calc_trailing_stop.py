"""
This script calculates the trailing stop percentage for a list of stock symbols.

Functions:
- calculate_percentage_difference(data): Calculates the percentage difference between today's low and previous day's close.
- read_symbols(filename): Reads stock symbols from a text file.
- process_symbols(symbols): Retrieves historical data and calculates the minimum and maximum percentage difference.
- main(): The main function that executes the script.

Usage:
1. Create a text file named 'symbols.txt' and add the stock symbols, each on a new line.
2. Run the script to calculate the trailing stop percentage for each symbol.
3. The script will display the results in a tabular format, showing the symbol, minimum percentage difference, maximum percentage difference, maximum drop from previous high, and last close price.

Note: The script uses the yfinance library to retrieve historical stock data.
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from tabulate import tabulate

# Function to calculate the percentage difference between today's low and previous day's close
def calculate_percentage_difference(data: pd.DataFrame) -> tuple:
    data['Prev Close'] = data['Close'].shift(1)
    data.dropna(inplace=True)
    data['Pct Difference'] = ((data['Low'] - data['Prev Close']) / data['Prev Close']) * 100
    return data['Pct Difference'].min(), data['Pct Difference'].max()

# Read stock symbols from a text file
def read_symbols(filename: str) -> list:
    with open(filename, 'r') as file:
        symbols = file.read().splitlines()
    return symbols

# Retrieve historical data and calculate min and max percentage difference
def process_symbols(symbols: list) -> dict:
    results = {}
    end_date = datetime.now()
    start_date = end_date - timedelta(days=6*30)  # Approximate 6 months
    for symbol in symbols:
        try:
            data = yf.download(symbol, start=start_date, end=end_date)
            # calculate the running high, based upon the close
            data['CumulativeHigh'] = data['Close'].cummax()
            # calculate the percentage difference between the close and the running high
            data['PctHigh'] = (data['Close'] - data['CumulativeHigh']) / data['CumulativeHigh'] * 100
            min_diff, max_diff = calculate_percentage_difference(data)
            results[symbol] = {
                'Min Difference': min_diff, 
                'Max Difference': max_diff, 
                'Max Drop from Prev High': data['PctHigh'].min(),
                'Last Close': data['Close'].iloc[-1]
                               }
        except Exception as e:
            results[symbol] = {'Error': str(e)}
    return results

# Main function
def main():
    filename = 'symbols.txt'  # Path to the file containing stock symbols
    symbols = read_symbols(filename)
    results = process_symbols(symbols)

    headers = ['Symbol', 'Min % Diff', 'Max % Diff', 'Max % Drop from High', 'Last Close']
    data = [(
        symbol, 
        result['Min Difference'], 
        result['Max Difference'], 
        result['Max Drop from Prev High'],
        result['Last Close']
        ) for symbol, result in results.items() if 'Error' not in result]
    print(tabulate(data, headers=headers))

if __name__ == "__main__":
    main()
