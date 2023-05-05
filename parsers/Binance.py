import pandas as pd
import time
from datetime import datetime
from binance.client import Client
import json
#обращение к настройкам, для подключения к бинанс
with open('C:/projects/parsing/params.json', 'r') as f:
    params = json.load(f)

#  API-ключ и секретный ключ
client = Client(api_key=params["binance"]["apikey"], api_secret=params["binance"]["secret"])


# Установление промежутка времени
start_date = datetime(2021, 5, 14)
end_date = datetime(2023, 4, 21)
time.sleep(2)
# Получение исторических данных о покупках и продажах биткоина
klines = client.get_historical_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, start_str=start_date.strftime("%d %b %Y %H:%M:%S"), end_str=end_date.strftime("%d %b %Y %H:%M:%S"))

# создание DataFrame и заполнение  данными о покупках и продажах
df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
df.columns = ['timestamp', 'open_price', 'high_price', 'low_price', 'close_price', 'volume']


# Сохранение данных в CSV-файл
df.to_csv('btcusdt_1m.csv', index=False)
time.sleep(2)