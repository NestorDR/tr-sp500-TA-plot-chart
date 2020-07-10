# -*- coding: utf-8 -*-

# Datetime: this module supplies classes for manipulating dates and times.
import datetime as dt
# Logging: module for tracking events that happen when some software runs.
import logging
# NumPy: library for array processing for numbers, strings, records, and objects.
import numpy as np
# Pandas: library for df analysis, which provides flexible df structures and efficient processing.
import pandas as pd
# Pandas_datareader: library to extract data from various Internet sources into a pandas DataFrame.
import pandas_datareader.data as web
# Time: this module offers time-related functions.
import time

from crosscutting import constants as const


class WebClient(object):
    """
    Infrastructure for data access
    """
    def __init__(self,
                 data_source_: str):
        """
        :param data_source_: data source to use.
        """
        self.data_source_ = data_source_.lower()

    def get_daily_data(self,
                       symbol_: str,
                       days_: int = 365) -> pd.DataFrame:
        """
        Returns daily historical prices on a pandas DataFrame

        :param symbol_: stock or instrument symbol to download prices.
        :param days_: Historical data period, where for example 30 means that historical prices are requested
                      for the last 30 days. Default value is 365.

        :return pandas.DataFrame with format [Open, High, Low, Close, Volume] index datetime

        Visit https://pandas-datareader.readthedocs.io/en/latest/remote_data.html

        Alternatively visit: https://github.com/dalenguyen/stockai
                             Python module to get stock data from Yahoo! Finance
        """
        # Format symbol
        symbol_ = symbol_.upper()

        # Set time window for downloading historical prices
        end_ = dt.date.today()
        start_ = end_ - dt.timedelta(days=days_)

        # Set the download start date to a minimum date: January-01-2000
        if start_ < dt.date(2000, 1, 1):
            start_ = dt.date(2000, 1, 1)

        if self.data_source_ == const.YAHOO:
            df_prices = self.__get_daily_yahoo(symbol_, start_, end_)
        else:
            logging.warning('Error: only YAHOO data source is supported for daily data.')
            df_prices = self.empty_df()

        # Returns historical prices
        return df_prices[['Open', 'High', 'Low', 'Close', 'Volume']]

    def get_intraday_data(self,
                          symbol_: str,
                          days_: int = 30) -> pd.DataFrame:
        """
        Returns intraday historical prices on a pandas DataFrame

        :param symbol_: stock or instrument symbol to download prices.
        :param days_: Historical data period, where for example 30 means that historical prices are requested
                      for the last 30 days. Default value is 30.

        :return pandas.DataFrame with format [Open, High, Low, Close, Volume] index datetime
        """

        logging.warning(f'To Do get_intraday_data for {self.data_source_}, {symbol_}({days_})')

        return self.empty_df()

    def __get_daily_yahoo(self, 
                          symbol_: str,
                          start_: dt.date,
                          end_: dt.date):
        """
        Returns daily historical prices from Yahoo! Finance on a pandas DataFrame. Private method.

        param symbol_: stock or instrument symbol to download prices.
        :param start_: start date of time window for downloading historical prices
        :param end_: end date of time window for downloading historical prices

        :return: pandas.DataFrame with format [Open, High, Low, Close, Volume] index datetime
        """

        # Initialize results
        df_prices = self.empty_df()

        # Repeat reading/downloading of data from the selected data source until successful,
        # or maximum number of attempts is reached
        attempts_ = 0
        while attempts_ < const.ATTEMPT_LIMIT:
            try:
                # Read ddtaframe from the data source
                df_prices = web.DataReader(symbol_, self.data_source_, start_, end_)
                break

            except Exception as exception_:
                attempts_ += 1
                if attempts_ == const.ATTEMPT_LIMIT:
                    # Logging error
                    logging.critical(f'Error during daily prices request for {symbol_} from '
                                     f'{self.data_source_.title()}.\n{type(exception_).__name__}\n{str(exception_)}')
                    # Returns empty df
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

        # Returns historical prices
        return df_prices[['Open', 'High', 'Low', 'Close', 'Volume']]

    @staticmethod
    def empty_df() -> pd.DataFrame:
        """
        :return: Empty pandas.DataFrame with format [Open, High, Low, Close, Volume]
        """
        return pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume'])


def main():
    # Initialize params.
    time_frame_ = const.INTRADAY
    symbol_ = const.SPX

    # Get historical prices
    if time_frame_ == const.DAILY:
        df_prices = WebClient(const.YAHOO).get_daily_data(symbol_, 300)
    elif time_frame_ == const.INTRADAY:
        df_prices = WebClient(const.ALPHA_VANTAGE).get_intraday_data(symbol_, 30)
    else:
        logging.warning('Error: time frame is not supported.')
        return

    # Save the prices to a CSV file
    df_prices.to_csv(symbol_ + '.CSV', encoding='utf-8', index_label='DateTime', sep=';', decimal=',',
                     float_format='%.3f')

    # Display first and last x records in console
    x = 10
    print(df_prices.head(x))
    print(df_prices.tail(x))


# Use of __name__ & __main__
# When the Python interpreter reads a code file, it completely executes the code in it.
# For example, in a my_module.py file, when executed as the main program, the __name__ attribute will be '__main__',
# however if used by importing from another module: import my_module, the __name__ attribute will be 'my_module'.
if __name__ == '__main__':
    main()
