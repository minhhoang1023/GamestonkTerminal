import logging
import os
from typing import List, Optional

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import ticker

from gamestonk_terminal.config_terminal import theme
from gamestonk_terminal import config_plot as cfgPlot
from gamestonk_terminal.cryptocurrency.due_diligence.coinglass_model import (
    get_open_interest_per_exchange,
)
from gamestonk_terminal.decorators import log_start_end
from gamestonk_terminal.helper_funcs import (
    export_data,
    long_number_format,
    plot_autoscale,
)
from gamestonk_terminal.rich_config import console

logger = logging.getLogger(__name__)


@log_start_end(log=logger)
def display_open_interest(symbol: str, interval: int, export: str) -> None:
    """Displays open interest by exchange for a certain cryptocurrency
    [Source: https://coinglass.github.io/API-Reference/]

    Parameters
    ----------
    symbol : str
        Crypto symbol to search open interest (e.g., BTC)
    interval : int
        Interval frequency (e.g., 0)
    export : str
        Export dataframe data to csv,json,xlsx file"""
    df = get_open_interest_per_exchange(symbol, interval)
    if df.empty:
        console.print("Error in coinglass request")
    else:
        plot_data(df, symbol)
    console.print("")

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "oi",
        df,
    )


@log_start_end(log=logger)
def plot_data(
    df: pd.DataFrame,
    symbol: str,
    external_axes: Optional[List[plt.Axes]] = None,
):

    # This plot has 2 axis
    if not external_axes:
        _, (ax1, ax2) = plt.subplots(
            2, 1, sharex=True, figsize=plot_autoscale(), dpi=cfgPlot.PLOT_DPI
        )
    else:
        if len(external_axes) != 2:
            console.print("[red]Expected list of two axis item./n[/red]")
            return
        ax1, ax2 = external_axes

    df_price = df[["price"]].copy()
    df_without_price = df.drop("price", axis=1)

    ax1.stackplot(
        df_without_price.index,
        df_without_price.transpose().to_numpy(),
        labels=df_without_price.columns.tolist(),
    )

    ax1.get_yaxis().set_major_formatter(
        ticker.FuncFormatter(lambda x, _: long_number_format(x))
    )
    ax1.legend(df_without_price.columns, fontsize="x-small", ncol=2)
    ax1.set_title(f"Exchange {symbol} Futures Open Interest")
    ax1.set_ylabel("Open futures value[$B]")

    ax2.plot(df_price.index, df_price)
    ax2.legend([f"{symbol} price"])
    ax2.set_ylabel(f"{symbol} Price [$]")
    ax2.set_xlim([df_price.index[0], df_price.index[-1]])
    ax2.set_ylim(bottom=0.0)

    theme.style_primary_axis(ax1)
    theme.style_primary_axis(ax2)

    if not external_axes:
        theme.visualize_output()
