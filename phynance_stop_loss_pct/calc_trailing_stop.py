import yfinance as yf
"""
This script calculates the trailing stop percentage difference for a list of stock symbols.

Functions:
- calculate_percentage_difference(data): Calculates the percentage difference between today's low and previous day's close.
- read_symbols(filename): Reads stock symbols from a text file.
- process_symbols(symbols): Retrieves historical data and calculates the minimum and maximum percentage difference for each symbol.
- main(): The main function that orchestrates the execution of the script.

Usage:
1. Ensure that the 'symbols.txt' file exists and contains the desired stock symbols.
2. Run the script to calculate the trailing stop percentage difference for each symbol.
3. The results will be printed in the console, including the minimum and maximum difference and the last close price for each symbol.
4. The results will also be displayed in a table format using the 'tabulate' library.

Note:
- If an error occurs while retrieving data for a symbol, the error message will be displayed instead of the difference values.
- The script uses the 'yfinance' library to retrieve historical stock data.
- The 'tabulate' library is used to display the results in a table format.
"""
from datetime import datetime, timedelta
from tabulate import tabulate

# Function to calculate the percentage difference between today's low and previous day's close
def calculate_percentage_difference(data):
    data['Prev Close'] = data['Close'].shift(1)
    data.dropna(inplace=True)
    data['Pct Difference'] = ((data['Low'] - data['Prev Close']) / data['Prev Close']) * 100
    return data['Pct Difference'].min(), data['Pct Difference'].max()

# Read stock symbols from a text file
def read_symbols(filename):
    with open(filename, 'r') as file:
        symbols = file.read().splitlines()
    return symbols

# Retrieve historical data and calculate min and max percentage difference
def process_symbols(symbols):
    results = {}
    end_date = datetime.now()
    start_date = end_date - timedelta(days=6*30)  # Approximate 6 months
    for symbol in symbols:
        try:
            data = yf.download(symbol, start=start_date, end=end_date)
            min_diff, max_diff = calculate_percentage_difference(data)
            results[symbol] = {'Min Difference': min_diff, 'Max Difference': max_diff, 'Last Close': data['Close'].iloc[-1]}
        except Exception as e:
            results[symbol] = {'Error': str(e)}
    return results

# Main function
def main():
    filename = 'symbols.txt'  # Path to the file containing stock symbols
    symbols = read_symbols(filename)
    results = process_symbols(symbols)

    headers = ['Symbol', 'Min % Diff', 'Max % Diff', 'Last Close']
    data = [(symbol, result['Min Difference'], result['Max Difference'], result['Last Close']) for symbol, result in results.items() if 'Error' not in result]
    print(tabulate(data, headers=headers))

if __name__ == "__main__":
    main()
