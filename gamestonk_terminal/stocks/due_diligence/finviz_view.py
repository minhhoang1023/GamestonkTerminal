""" Finviz View """
__docformat__ = "numpy"

import logging
import os
from typing import Any, List

from gamestonk_terminal import feature_flags as gtff
from gamestonk_terminal.decorators import log_start_end
from gamestonk_terminal.helper_funcs import export_data, print_rich_table
from gamestonk_terminal.rich_config import console
from gamestonk_terminal.stocks.due_diligence import finviz_model

logger = logging.getLogger(__name__)


@log_start_end(log=logger)
def category_color_red_green(val: str) -> str:
    """Add color to analyst rating

    Parameters
    ----------
    val : str
        Analyst rating - Upgrade/Downgrade

    Returns
    -------
    str
        Analyst rating with color
    """

    if val == "Upgrade":
        return f"[green]{val}[/green]"
    if val == "Downgrade":
        return f"[red]{val}[/red]"
    if val == "Reiterated":
        return f"[yellow]{val}[/yellow]"
    return val


@log_start_end(log=logger)
def news(ticker: str, num: int):
    """Display news for a given stock ticker

    Parameters
    ----------
    ticker : str
        Stock ticker
    fnews : int
        Number of latest news being printed
    """
    fnews: List[Any] = finviz_model.get_news(ticker)

    if fnews:
        fnews = sorted(fnews, reverse=True)[:num]

        for news_date, news_title, news_link, _ in fnews:
            console.print(f"{news_date} - {news_title}")
            console.print(f"{news_link}\n")

    else:
        console.print("No news found for this ticker")


@log_start_end(log=logger)
def analyst(ticker: str, export: str = ""):
    """Display analyst ratings. [Source: Finviz]

    Parameters
    ----------
    ticker : str
        Stock ticker
    export : str
        Export dataframe data to csv,json,xlsx file
    """
    df = finviz_model.get_analyst_data(ticker)

    if gtff.USE_COLOR:
        df["category"] = df["category"].apply(category_color_red_green)

    print_rich_table(
        df, headers=list(df.columns), show_index=True, title="Display Analyst Ratings"
    )

    console.print("")
    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "analyst",
        df,
    )
