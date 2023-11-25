from tradingview_ta import TA_Handler, Interval
import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta


def listeyi_guncelle():
    url = 'https://www.getmidas.com/canli-borsa/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    hisse_tablosu = soup.find('table', attrs={"class": "stock-table w-100"})
    tablo_satirlari = hisse_tablosu.findAll("tr", attrs={"class": "table-row"})

    hisse_listesi = []
    for i in range(len(tablo_satirlari)):
        hisse_adi = tablo_satirlari[i].find("a", attrs={"class": "title stock-code"}).text
        hisse_listesi.append(hisse_adi)

    df = pd.DataFrame(hisse_listesi, columns=['Hisse'])
    df.set_index("Hisse", inplace=True)
    return df


def get_stock_data(stock):
    info = TA_Handler(
        symbol=stock,
        screener="turkey",
        exchange="BIST",
        interval=Interval.INTERVAL_1_DAY,
    )
    return pd.DataFrame(data=[[stock,
                               info.get_indicators().get('open'),
                               info.get_indicators().get('high'),
                               info.get_indicators().get('low'),
                               info.get_indicators().get('close'),
                               info.get_indicators().get('change'),
                               ]], columns=['Stock', 'Open', 'High', 'Low', 'Close', 'Change'])


def get_historical_prices(stock):
    end = datetime.now()
    start = end - timedelta(days=30)
    data = yf.download(stock + '.IS', start=start, end=end)
    data.index = pd.to_datetime(data.index).tz_localize('UTC')
    return data['Close']
