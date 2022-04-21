from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import pandas as pd

apikey='MZoUNKZin6hLFAaPtMyi0GrZXjz8ca55OL4Qlmys3YuUOSzS6fdtW97WvlKzs5yA'
secret='QuIoCo9pTkb8hw1ktIXZoxtPKnG9e2kXYCLy05c876aHqA4NL1T4s5ZAWtD2q9y4'

client=Client(apikey,secret)

tickers=client.get_all_tickers()

print(tickers)