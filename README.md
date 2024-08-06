# phynance-stop-loss-pct

Finds previous daily drops for given stocks and ETFs

This script will read stock symbols from symbols.txt, retrieve historical data for the last six months, calculate the percentage difference between each day's low and the previous day's close, and then print the minimum and maximum percentage differences for each stock.