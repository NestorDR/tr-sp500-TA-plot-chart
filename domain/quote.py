# -*- coding: utf-8 -*-

# Logging: module for tracking events that happen when some software runs.
import logging
# Pandas: library for df analysis, which provides flexible df structures and efficient processing.
import pandas as pd

from crosscutting import constants as const
from infrastructure import integration


class Service(object):
    """
    Domain services for the entity Quotes for investment instruments
    """

    def __init__(self,
                 time_frame_: str):
        self.time_frame = time_frame_.lower()
        if self.time_frame == const.DAILY:
            self.data_source = const.YAHOO
        elif self.time_frame == const.INTRADAY:
            self.data_source = const.ALPHA_VANTAGE
        else:
            self.data_source = None
        self.__symbol_ = ''

    def get_prices(self,
                   symbol_: str,
                   days_: int = None) -> pd.DataFrame:
        """
        Returns historical prices on a pandas DataFrame

        :param symbol_: stock or instrument symbol to download prices.
        :param days_: Historical data period, where for example 30 means that historical prices are requested
                      for the last 30 days. Default value is 365.

        :return pandas.DataFrame with format [Open, High, Low, Close, Volume] index datetime
        """
        symbol_ = self.__equiv_symbol(symbol_, self.data_source)
        web_ = integration.WebClient(self.data_source)

        if self.time_frame == const.DAILY:
            if days_ is None:
                days_ = 365
            df_prices = web_.get_daily_data(symbol_, days_)
        elif self.time_frame == const.INTRADAY:
            df_prices = web_.get_intraday_data(symbol_, 30)
        else:
            logging.warning('Error: time frame is not supported.')
            df_prices = web_.empty_df()

        # Round to 4 decimal places
        df_prices['Open'].apply(lambda n: round(n, 4))
        df_prices['High'].apply(lambda n: round(n, 4))
        df_prices['Low'].apply(lambda n: round(n, 4))
        df_prices['Close'].apply(lambda n: round(n, 4))

        return df_prices

    @staticmethod
    def __equiv_symbol(symbol_: str,
                       to_data_source_: str) -> str:
        """
        Identifies equivalent symbol for the online selected data source/data provider

        :param symbol_: stock or instrument symbol to download prices.
        :param to_data_source_: online data source to which the symbol for data download will be equivalent

        :return: Symbol in the selected data provider
        """

        if to_data_source_ == const.YAHOO:
            # Make symbol equivalent to Yahoo notation
            if symbol_ in ['.INX', 'SPX']:
                symbol_ = '^GSPC'
            elif symbol_ in ['NDX', 'RMZ', 'RUT', 'TNX', 'VIX', 'NYFANG']:
                symbol_ = f'^{symbol_}'
            elif symbol_[0] == '.':
                symbol_ = symbol_.replace('.', '^')

        elif to_data_source_ == const.ALPHA_VANTAGE:
            # Make symbol equivalent to Alpha Vantage notation
            if symbol_ in ['.INX', '^GSPC']:
                symbol_ = 'SPX'
            elif symbol_[0] == '.':
                symbol_ = symbol_.replace('.', '')

        elif to_data_source_ == const.GOOGLE:
            # Make symbol equivalent to Google notation
            if symbol_ in ['^GSPC', 'SPX']:
                symbol_ = '.INX'
            elif symbol_ in ['^DJI', '^IXIC']:
                symbol_ = symbol_.replace('^', '.')
            elif symbol_ == 'DJI':
                symbol_ = '.DJI'
            elif symbol_ in ['^NDX', '^RMZ', '^RUT', '^TNX', '^VIX', '^NYFANG']:
                symbol_ = symbol_.replace('^', '')
            elif symbol_ == '^MERV':
                symbol_ = 'IMV'

        return symbol_


def main():
    # Initialize params.
    time_frame_ = const.DAILY
    symbol_ = const.SPX

    # Get historical prices
    df_prices = Service(time_frame_).get_prices(symbol_)

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
