# -*- coding: utf-8 -*-

# Pandas: library for df analysis, which provides flexible df structures and efficient processing.
import pandas as pd


def reset_pd_display():
    """
    Configures the output to display fragments of the DataFrames
    """
    pd.options.display.max_rows = -1
    pd.options.display.float_format = '{:.2f}'.format
    pd.options.display.max_columns = None
    pd.options.display.expand_frame_repr = False
    pd.options.display.max_colwidth = -1

