

# =============================================================================
# #%% Install packages 
# !pip install pycoingecko
# !pip install plotly
# !pip install mplfinance
# !pip install kaleido
# =============================================================================
#%%  Import labrairies 
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.offline import plot
import matplotlib.pyplot as plt
import datetime
from pycoingecko import CoinGeckoAPI
from mplfinance.original_flavor import candlestick2_ohlc

import plotly.io as pio

#%% 
cg = CoinGeckoAPI()
#print("type cg is", type(cg))

bitcoin_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=30)
#print('type bitcoin_data is', type(bitcoin_data))

# Bitcoin data price 
bitcoin_price_data = bitcoin_data['prices']


bitcoin_price_data[0:5]

# transform the dat to data frame 
data = pd.DataFrame(bitcoin_price_data, columns=['TimeStamp', 'Price'])
#print ("type of dat is", type(data))
data.head()

"""Convert the timestamp to datetime and save it as a column called Date"""
    
data['date'] = data['TimeStamp'].apply(lambda d: datetime.date.fromtimestamp(d/1000.0))

#%% Group by the Date and find the min, max, open, and close for the candlesticks

candlestick_data = data.groupby(data.date, as_index=False).agg({"Price": ['min', 'max', 'first', 'last']})
print("candlestick_data", candlestick_data.head())



#%% use plotly to create our Candlestick Chart.

pio.renderers.default = 'browser'

#pio.renderers.default = 'browser'

fig = go.Figure(data=[go.Candlestick(x=candlestick_data['date'],
                open=candlestick_data['Price']['first'], 
                high=candlestick_data['Price']['max'],
                low=candlestick_data['Price']['min'], 
                close=candlestick_data['Price']['last'])
                ])

fig.update_layout(xaxis_rangeslider_visible=True)

fig.show()

