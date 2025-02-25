"""Screener context API."""
import os
from gamestonk_terminal.helper_classes import ModelsNamespace as _models

# flake8: noqa
# pylint: disable=unused-import

# Context menus
from gamestonk_terminal.etf.screener.screener_view import view_screener as screen

# Models
models = _models(os.path.abspath(os.path.dirname(__file__)))
