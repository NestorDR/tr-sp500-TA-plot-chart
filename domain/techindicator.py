# -*- coding: utf-8 -*-

# Logging: module for tracking events that happen when some software runs.
import logging
# Pandas: library for df analysis, which provides flexible df structures and efficient processing.
import pandas as pd
# TA-Lib: library for technical stock market analysis. It's a Python wrapper for TA-LIB based on Cython.
from talib import func


def add_moving_average(df: pd.DataFrame,
                       mat_window_: list):
    """
    Adds moving averages columns to the DataFrame of historical prices

    :param df: pandas.Dataframe with historical prices
    :param mat_window_: list [moving average type, time window] defining moving averages to calculate
                Example ma_type_window_ = [['EMA', 13], ['WMA', 55]]
    """
    for ma_ in mat_window_:
        # Extract params
        ma_type_, time_window_ = ma_
        ma_type_ = ma_type_.upper()
        column_name_ = f'{ma_type_.title()}{time_window_:0>2}'

        # Identify, calculate and add moving average column to the DataFrame
        if ma_type_ == 'SMA':               # Simple Moving Average
            # Visit https://www.investopedia.com/terms/s/sma.asp
            df[column_name_] = df['Close'].rolling(window=time_window_).mean()
        elif ma_type_ == 'EMA':             # Exponential Moving Average
            # Visit https://www.investopedia.com/terms/e/ema.asp
            df[column_name_] = func.EMA(df['Close'], time_window_)
        elif ma_type_ == 'WMA':             # Weighted Moving Average
            # Visit https://www.investopedia.com/terms/l/linearlyweightedmovingaverage.asp
            df[column_name_] = func.WMA(df['Close'], time_window_)
        else:
            logging.warning(f'ERROR: Calculation of moving average: {ma_type_}, not supported.')


def add_tech_indicator(df: pd.DataFrame,
                       tai_window_: list):
    """
    Adds technical analysis indicators columns to the DataFrame of historical prices

    :param df: pandas.Dataframe with historical prices
    :param tai_window_: list [technical indicator type, time window] defining technical analysis indicators to calculate
                Example tai_window_ = [['RSI', 14], ['MACD', (12, 26, 9)]]
    """

    for ti_ in tai_window_:
        # Extract params
        ti_type_, time_window_ = ti_
        ti_type_ = ti_type_.upper()
        column_name_ = f'{ti_type_.title()}'

        # Identify, calculate and add technical analysis indicator column(s) to the DataFrame
        if ti_type_ == 'RSI':               # Relative Strength Index (Momentum Indicators)
            # Visit https://www.investopedia.com/terms/r/rsi.asp
            df[column_name_] = func.RSI(df['Close'], time_window_)
        elif ti_type_ == 'MACD':            # Moving Average Convergence/Divergence (Momentum Indicators)
            # Visit https://www.investopedia.com/terms/m/macd.asp
            fast_period_, slow_period_, signal_period_ = time_window_
            df[column_name_], df[f'{column_name_}Signal'], df[f'{column_name_}Histogram'] =\
                func.MACD(df['Close'], fast_period_, slow_period_, signal_period_)
        elif ti_type_ == 'UO':              # Ultimate Oscillator (Momentum Indicators)
            # Visit https://www.investopedia.com/terms/u/ultimateoscillator.asp
            first_time_period_, second_timeperiod_, third_time_period_ = time_window_
            df[column_name_] = func.ULTOSC(df['High'], df['Low'], df['Close'],
                                           first_time_period_, second_timeperiod_, third_time_period_)

        else:
            logging.warning(f'ERROR: Calculation of technical analysis indicator: {ti_type_}, not supported.')
            continue
