import talib
import personal_function as pf

client=pf.client()

symbol='BTCUSDT'
interval='4h'
start_date="1 Jan, 2020"
end_date="31 Dec, 2020"
KlinesType='SPOT'

data=pf.historical_data(client, symbol,interval, start_date, end_date,KlinesType)


morning_star = talib.CDLMORNINGSTAR(data['Open'], data['High'], data['Low'], data['Close'])

engulfing = talib.CDLENGULFING(data['Open'], data['High'], data['Low'], data['Close'])

data['Morning Star'] = morning_star
data['Engulfing'] = engulfing

engulfing_days = data[data['Engulfing'] != 0]


print(engulfing_days)