import pandas_datareader as web
from pandas_datareader.nasdaq_trader import get_nasdaq_symbols
from tqdm import tqdm

symbols=get_nasdaq_symbols()
print(symbols.head())