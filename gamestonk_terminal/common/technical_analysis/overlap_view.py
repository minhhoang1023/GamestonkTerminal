"""TA Overlap View"""
__docformat__ = "numpy"

import os
from typing import List

import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
from pandas.plotting import register_matplotlib_converters

from gamestonk_terminal import config_terminal as cfg
import gamestonk_terminal.feature_flags as gtff
from gamestonk_terminal.common.technical_analysis import overlap_model
from gamestonk_terminal.config_plot import PLOT_DPI
from gamestonk_terminal.helper_funcs import export_data, plot_autoscale
from gamestonk_terminal.rich_config import console

register_matplotlib_converters()


def view_ma(
    values: pd.Series,
    length: List[int] = None,
    offset: int = 0,
    ma_type: str = "EMA",
    s_ticker: str = "",
    export: str = "",
) -> pd.DataFrame:
    """Plots MA technical indicator

    Parameters
    ----------
    values : pd.Series
        Series of prices
    length : List[int]
        Length of EMA window
    ma_type: str
        Type of moving average.  Either "EMA" "ZLMA" or "SMA"
    s_ticker : str
        Ticker
    export : str
        Format to export data
    """
    # Define a dataframe for adding EMA values to it
    price_df = pd.DataFrame(values)

    l_legend = [s_ticker]
    if not length:
        length = [20, 50]

    for win in length:
        if ma_type == "EMA":
            df_ta = overlap_model.ema(values, win, offset)
            l_legend.append(f"EMA {win}")
        elif ma_type == "SMA":
            df_ta = overlap_model.sma(values, win, offset)
            l_legend.append(f"SMA {win}")
        elif ma_type == "WMA":
            df_ta = overlap_model.wma(values, win, offset)
            l_legend.append(f"WMA {win}")
        elif ma_type == "HMA":
            df_ta = overlap_model.hma(values, win, offset)
            l_legend.append(f"HMA {win}")
        elif ma_type == "ZLMA":
            df_ta = overlap_model.zlma(values, win, offset)
            l_legend.append(f"ZLMA {win}")
        price_df = price_df.join(df_ta)

    fig, ax = plt.subplots(figsize=plot_autoscale(), dpi=PLOT_DPI)
    ax.set_title(f"{s_ticker} {ma_type.upper()}")

    ax.plot(values.index, values.values, linewidth=1)

    ax.set_xlabel("Time")
    ax.set_xlim([price_df.index[0], price_df.index[-1]])
    ax.tick_params(axis="x", rotation=10)

    ax.set_ylabel(f"{s_ticker} Price")
    ax.yaxis.set_label_position("right")

    for idx in range(1, price_df.shape[1]):
        ax.plot(price_df.iloc[:, idx])

    ax.legend(l_legend)
    ax.grid(b=True, which="major", linestyle=":")

    if gtff.USE_ION:
        plt.ion()

    fig.tight_layout(pad=1)

    plt.show()
    console.print("")

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)).replace("common", "stocks"),
        f"{ma_type.lower()}{'_'.join([str(win) for win in length])}",
        price_df,
    )


def view_vwap(
    s_ticker: str,
    df_stock: pd.DataFrame,
    offset: int = 0,
    s_interval: str = "",
    export: str = "",
):
    """Plots EMA technical indicator

    Parameters
    ----------
    s_ticker : str
        Ticker
    df_stock : pd.DataFrame
        Dataframe of prices
    offset : int
        Offset variable
    s_interval : str
        Interval of data
    export : str
        Format to export data
    """

    df_stock.index = df_stock.index.tz_localize(None)
    df_stock["Day"] = [idx.date() for idx in df_stock.index]

    day_df = df_stock[df_stock.Day == df_stock.Day[-1]]

    df_vwap = overlap_model.vwap(day_df, offset)

    addplot_result = mpf.make_addplot(df_vwap)

    if gtff.USE_ION:
        plt.ion()

    fig, _ = mpf.plot(
        day_df,
        type="candle",
        style=cfg.style.mpf_style,
        volume=True,
        addplot=addplot_result,
        xrotation=10,
        figratio=(10, 7),
        figscale=1.10,
        scale_padding={"left": 0.3, "right": 1.2, "top": 0.8, "bottom": 0.8},
        figsize=(plot_autoscale()),
        update_width_config=dict(
            candle_linewidth=0.6,
            candle_width=0.8,
            volume_linewidth=0.8,
            volume_width=0.8,
        ),
        returnfig=True,
    )
    fig.suptitle(
        f"{s_ticker} {s_interval} VWAP",
        x=0.055,
        y=0.965,
        horizontalalignment="left",
    )
    console.print("")

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)).replace("common", "stocks"),
        "VWAP",
        df_vwap,
    )
