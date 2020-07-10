## Description

This example allows you to build technical analysis charts for indices, stocks, cryptocurrencies and more, from zero, with Python.

A [Japanese candlestick chart](https://en.wikipedia.org/wiki/Candlestick_chart) is versatile style of financial chart used to describe price movements. If we add occidental analysis techniques, and even more, the forescast of machine learning models, we could have a solid tool to help us in the market surfing.

This example implements perhaps the most common architecture pattern which is [n-tier architecture pattern](https://www.oreilly.com/library/view/software-architecture-patterns/9781491971437/ch01.html). And it has a lot of comments within its code.

![Three-Tier architecture pattern](/assets/arquitecture.svg "Three-Tier architecture pattern")

### Infrastructure

The infrastructure layer, also known data access tier, encapsulates the acquisition of daily historical stock prices over Yahoo! Finance. To do it, uses [pandas_datareader](https://pypi.org/project/pandas-datareader/) library which allows to extract data from various Internet sources into a Pandas DataFrame. 

````python
# Pandas_datareader: library to extract data from various Internet sources into a pandas DataFrame.
import pandas_datareader.data as web
...
# Read ddtaframe from the data source
df_prices = web.DataReader(symbol_, self.data_source_, start_, end_)
````   

### Domain

The domain layer, also known as the business logic level, manages how prices are obtained and allows us to add the desired technical analysis indicators. To do it, uses [TA-lib](https://ta-lib.org), which is a technical analysis library for financial market data sets, expressed as time series.

If you have problems to install TA-Lib, please visit [How to install TA-Lib in Python](https://blog.quantinsti.com/install-ta-lib-python/#windows).

````python
# TA-Lib: library for technical stock market analysis. It's a Python wrapper for TA-LIB based on Cython.
from talib import func
...
# Identify, calculate and add technical analysis indicator column(s) to the DataFrame
df[column_name_] = func.EMA(df['Close'], time_window_)
...
# Identify, calculate and add technical analysis indicator column(s) to the DataFrame
df[column_name_] = func.RSI(df['Close'], time_window_)
````

### Presentation

The UI layer or presentation tier is the user interface. It does not know or worry about how to get financial data or technical indicators; it only needs to display that information on a screen in particular format. To do it, it uses [Plotly](https://plotly.com/python/candlestick-charts/), which is a advanced UI layer for ML and data science models, allowing him to build interactive candlestick charts in Python.

````python
# Plotly: library to make interactive charts. Visit https://plotly.com
from plotly import graph_objects as go, subplots
...
# Create chart with subplots
fig = subplots.make_subplots(rows=3, cols=1,
                             row_heights=[0.7, 0.15, 0.15],
                             shared_xaxes=True,
                             vertical_spacing=0.005)

# Add candlestick graphic object to plotly visualization
go_candlestick_ = go.Candlestick(x=df.index,
                                 open=df['Open'],
                                 high=df['High'],
                                 low=df['Low'],
                                 close=df['Close'],
                                 name=title_)
fig.add_trace(go_candlestick_, row=subplot_row_, col=1)
...
````

## Requirements
````console
$ python --version  
Python 3.7.1  
$ pip install -r requirements.txt
numpy==1.19
pandas==0.24.2
pandas-datareader==0.8.1
plotly==4.8.2
TA-Lib==0.4.17
````

## Execution
````console
$ python plotchart.py  
````
