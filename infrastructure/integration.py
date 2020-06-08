# -*- coding: utf-8 -*-

# Datetime: this module supplies classes for manipulating dates and times.
import datetime as dt
# Logging: module for tracking events that happen when some software runs.
import logging
# NumPy: library for array processing for numbers, strings, records, and objects.
import numpy as np
# Pandas: library for df analysis, which provides flexible df structures and efficient processing.
import pandas as pd
# Pandas_datareader: library to extract df from various Internet sources into a pandas DataFrame.
import pandas_datareader.data as web
# Time: this module offers time-related functions.
import time

from constants import ATTEMPT_LIMIT, DAILY, INTRADAY, YAHOO


class WebClient(object):
    """
    Infrastructure for df access
    """
    def __init__(self,
                 data_source_: str = YAHOO):
        """
        :param data_source_: df source to use. Default value is YAHOO.
        """
        self.data_source_ = data_source_.lower()

    def get_daily_data(self,
                       symbol_: str,
                       days_: int = 30) -> pd.DataFrame:
        """
        Returns daily historical prices on a pandas DataFrame

        :param symbol_: stock or instrument symbol to download prices.
        :param days_: Historical df period, where for example 30 means that historical prices are requested
                      for the last 30 days. Default value is 30.

        :return pandas.DataFrame: format [Symbol, Open, High, Low, Close, Volume] index datetime

        Visit https://pandas-datareader.readthedocs.io/en/latest/remote_data.html

        Alternatively visit: https://github.com/dalenguyen/stockai
                             Python module to get stock df from Yahoo! Finance
        """
        # Initialize output variable
        df_prices = pd.DataFrame()

        if self.data_source_ != YAHOO:
            logging.warning('Error: only YAHOO df source is supported for daily df.')
            # Returns df = None
            return df_prices

        # Format symbol
        symbol_ = symbol_.upper()

        # Set time window for downloading historical prices
        end_ = dt.date.today()
        start_ = end_ - dt.timedelta(days=days_)

        # Set the download start date to a minimum date: January-01-2000
        if start_ < dt.date(2000, 1, 1):
            start_ = dt.date(2000, 1, 1)

        # Repeat reading/downloading of df from the selected df source until successful,
        # or maximum number of attempts is reached
        attempts_ = 0
        while attempts_ < ATTEMPT_LIMIT:
            try:
                # Read df from the df source
                df_prices = web.DataReader(symbol_, self.data_source_, start_, end_)
                break

            except Exception as exception_:
                attempts_ += 1
                if attempts_ == ATTEMPT_LIMIT:
                    # Logging error
                    logging.critical(f'Error during daily prices request for {symbol_} from '
                                     f'{self.data_source_.title()}.\n{type(exception_).__name__}\n{str(exception_)}')
                    # Returns df = None
                    return df_prices
                else:
                    # Wait a few seconds before retrying
                    time.sleep(3)

        # Remove rows without values
        df_prices = df_prices[~np.isnan(df_prices["Close"])]

        # Adjust OHLC according to Adj Close
        df_prices['Factor'] = df_prices['Adj Close'] / df_prices['Close']
        df_prices['Open'] = df_prices['Open'] * df_prices['Factor']
        df_prices['High'] = df_prices['High'] * df_prices['Factor']
        df_prices['Close'] = df_prices['Close'] * df_prices['Factor']
        df_prices['Low'] = df_prices['Low'] * df_prices['Factor']

        # Round to 4 decimal places
        df_prices['Open'].apply(lambda n: round(n, 4))
        df_prices['High'].apply(lambda n: round(n, 4))
        df_prices['Low'].apply(lambda n: round(n, 4))
        df_prices['Close'].apply(lambda n: round(n, 4))

        # Returns historical prices
        return df_prices[['Open', 'High', 'Low', 'Close', 'Volume']]


def main():
    time_period_ = DAILY
    symbol_ = '^GSPC'

    if time_period_ == DAILY:
        df_prices = WebClient(YAHOO).get_daily_data(symbol_, 300)
    elif time_period_ == INTRADAY:
        print('To Do get_intraday_data')
        df_prices = pd.DataFrame()
        # df = integrationclient(ALPHA_VANTAGE).get_intraday_data(symbol_, 1, 30)
    else:
        print('Time interval not supported')
        return

    # Save the prices to a CSV file
    df_prices.to_csv(symbol_ + '.CSV', encoding='utf-8', index_label='DateTime', sep=';', decimal=',',
                     float_format='%.3f')

    # Display first and last x records in console
    x = 15
    print(df_prices.head(x))
    print(df_prices.tail(x))


# Use of __name__ & __main__
# When the Python interpreter reads a code file, it completely executes the code in it.
# For example, in a my_module.py file, when executed as the main program, the __name__ attribute will be '__main__',
# however if used by importing from another module: import my_module, the __name__ attribute will be 'my_module'.
if __name__ == '__main__':
    main()
