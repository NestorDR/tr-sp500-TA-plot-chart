# -*- coding: utf-8 -*-

# Pandas: library for df analysis, which provides flexible df structures and efficient processing.
import pandas as pd
# Plotly: library to make interactive charts. Visit https://plotly.com
from plotly import graph_objects as go, subplots

import crosscutting
from domain import quote, techindicator
from crosscutting import constants as const


def plot_chart(df: pd.DataFrame,
               mat_window_: list,
               tai_window_: list,
               title_: str):
    """
    Plot chart with Plotly.graph_objects

    :param df: pandas.Dataframe with historical prices and technical analysis indicators
    :param mat_window_: list [moving average type, time window] defining moving averages to plot
                Example mat_window_ = [['EMA', 13], ['WMA', 55]]
    :param tai_window_: list [technical indicator type, time window] defining technical analysis indicators to plot
                Example tai_window_ = [['RSI', 14], ['MACD', (12, 26, 9)]]
    :param title_: chart title
    """

    # Create chart with subplots
    fig = subplots.make_subplots(rows=3, cols=1,
                                 row_heights=[0.7, 0.15, 0.15],
                                 shared_xaxes=True,
                                 vertical_spacing=0.005)

    # Set subplot row to use
    subplot_row_ = 1

    # Add candlestick graphic object to plotly visualization
    # Visit https://plotly.com/python/candlestick-charts/
    go_candlestick_ = go.Candlestick(x=df.index,
                                     open=df['Open'],
                                     high=df['High'],
                                     low=df['Low'],
                                     close=df['Close'],
                                     name=title_)
    fig.add_trace(go_candlestick_, row=subplot_row_, col=1)

    # Add graphic objects of the moving averages to plotly visualization
    for ma_ in mat_window_:
        # Extract params
        ma_type_, time_window_ = ma_
        column_name_ = f'{ma_type_.title()}{time_window_:0>2}'
        # Add graphic object of the moving average to plotly visualization
        go_ma_ = go.Scatter(x=df.index,
                            y=df[column_name_],
                            line=dict(width=1),
                            name=f'{ma_type_.upper()}({time_window_})')
        fig.add_trace(go_ma_, row=subplot_row_, col=1)

    # Add graphic objects of the technical analysis indicators to plotly visualization
    for ti_ in tai_window_:
        # Extract params
        ti_type_, time_window_ = ti_
        ti_type_ = ti_type_.upper()
        column_name_ = f'{ti_type_.title()}'

        if ti_type_ == 'MACD':
            # Set subplot row to use
            subplot_row_ = subplot_row_ + 1

            # Add graphic object of the technical analysis indicator to plotly visualization
            fastperiod_, slowperiod_, signalperiod_ = time_window_
            go_ti_ = go.Scatter(x=df.index,
                                y=df[column_name_],
                                line=dict(color='rgba(0, 0, 255, 0.5)', width=1),
                                mode='lines',
                                name=f'{ti_type_.upper()}({fastperiod_}, {slowperiod_})')
            fig.add_trace(go_ti_, row=subplot_row_, col=1)
            go_ti_ = go.Scatter(x=df.index,
                                y=df[f'{column_name_}Signal'],
                                line=dict(color='rgba(255, 0, 0, 0.5)', width=1),
                                mode='lines',
                                name=f'{ti_type_.upper()} Signal({signalperiod_})')
            fig.add_trace(go_ti_, row=subplot_row_, col=1)
            go_ti_ = go.Bar(x=df.index,
                            y=df[f'{column_name_}Histogram'],
                            marker=dict(color='rgba(114, 160, 193, 0.8)'),
                            name=f'{ti_type_.upper()} Histogram')
            fig.add_trace(go_ti_, row=subplot_row_, col=1)
            go_00_ = go.Scatter(x=df.index,
                                y=[0] * len(df.index),
                                line=dict(color='rgba(0, 0, 0, 0.3)', width=1),
                                showlegend=False)
            fig.add_trace(go_00_, row=subplot_row_, col=1)

        elif ti_type_ == 'RSI':
            # Set subplot row to use
            subplot_row_ = subplot_row_ + 1

            # Add graphic object of the technical analysis indicator to plotly visualization
            go_ti_ = go.Scatter(x=df.index,
                                y=df[column_name_],
                                line=dict(color='rgba(51, 02, 102, 0.7)', width=1),
                                name=f'{ti_type_.upper()}({time_window_})')
            fig.add_trace(go_ti_, row=subplot_row_, col=1)
            go_30_ = go.Scatter(x=df.index,
                                y=[30] * len(df.index),
                                line=dict(color='rgba(51, 02, 102, 0.2)', width=1),
                                showlegend=False)
            fig.add_trace(go_30_, row=subplot_row_, col=1)
            go_70_ = go.Scatter(x=df.index,
                                y=[70] * len(df.index),
                                line=dict(color='rgba(51, 02, 102, 0.2)', width=1),
                                showlegend=False)
            fig.add_trace(go_70_, row=subplot_row_, col=1)

        elif ti_type_ == 'UO':
            # Set subplot row to use
            subplot_row_ = subplot_row_ + 1

            # Add graphic object of the technical analysis indicator to plotly visualization
            go_ti_ = go.Scatter(x=df.index,
                                y=df[column_name_],
                                line=dict(color='rgba(255, 165, 0, 0.5)', width=1),
                                name=f'{ti_type_.upper()}({time_window_})')
            fig.add_trace(go_ti_, row=subplot_row_, col=1)

        if subplot_row_ > 3:
            break

    fig.update_layout(title_text=title_,
                      margin=dict(t=40, b=5, l=5, r=5),
                      paper_bgcolor="LightSteelBlue",
                      xaxis_rangeslider_visible=False)
    fig.update_xaxes(automargin=True,
                     showline=True,
                     linewidth=1,
                     linecolor='black',
                     mirror=True,
                     rangebreaks=[
                         dict(bounds=['sat', 'mon']),                                   # hide weekends
                         dict(values=['2020-01-01', '2020-04-10', '2020-05-25'])])      # hide holydays
    fig.update_yaxes(automargin=True,
                     showline=True,
                     linewidth=1,
                     linecolor='black',
                     mirror=True)

    # Display chart
    fig.show()


# Use of __name__ & __main__
# When the Python interpreter reads a code file, it completely executes the code in it.
# For example, in a my_module.py file, when executed as the main program, the __name__ attribute will be '__main__',
# however if used by importing from another module: import my_module, the __name__ attribute will be 'my_module'.
if __name__ == '__main__':

    # Initialize params.
    time_frame_ = const.DAILY
    symbol_ = const.SPX
    days_for_downloading_ = 600
    verbose_ = 2

    # Gets historical prices
    quote = quote.Quote(time_frame_)
    df_data = quote.get_prices(symbol_, days_for_downloading_)

    # Release resources
    del quote

    # Set list [moving average type, time window] for define moving averages to calculate
    mat_window_params_ = [['EMA', 34], ['SMA', 200]]
    # Add moving averages to the DataFrame of historical prices
    techindicator.add_moving_average(df_data, mat_window_params_)

    # Set list [technical indicator type, time window] for define technical analysis indicators to calculate
    tai_window_params_ = [['RSI', 14], ['MACD', (12, 26, 9)]]
    # Add tecnical analysis indicators to the DataFrame of historical prices
    techindicator.add_tech_indicator(df_data, tai_window_params_)

    if verbose_ > 0:
        # Display first and last x records in console
        x = 5
        crosscutting.reset_pd_display()
        print(df_data.head(x))
        print(df_data.tail(x))

    # Filter number of bars to plot
    number_bars_ = 120
    # Set chart title
    if symbol_ == const.SPX:
        chart_title_ = 'S&P 500'
    elif symbol_ == const.DJI:
        chart_title_ = 'Dow Jones Industrial Average'
    else:
        chart_title_ = symbol_

    # Plot
    plot_chart(df_data.iloc[-number_bars_:], mat_window_params_, tai_window_params_, chart_title_)
