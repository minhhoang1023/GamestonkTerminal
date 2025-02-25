# IMPORTATION STANDARD

# IMPORTATION THIRDPARTY
import pandas as pd
import pytest

# IMPORTATION INTERNAL
from gamestonk_terminal.cryptocurrency.discovery import coinmarketcap_view


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": [("X-CMC_PRO_API_KEY", "MOCK_X_CMC_PRO_API_KEY")],
    }


@pytest.mark.vcr
@pytest.mark.record_stdout
def test_display_cmc_top_coins(mocker):
    # MOCK EXPORT_DATA
    mocker.patch(
        target="gamestonk_terminal.cryptocurrency.discovery.coinmarketcap_view.export_data"
    )

    coinmarketcap_view.display_cmc_top_coins()


@pytest.mark.vcr
@pytest.mark.record_stdout
def test_display_cmc_top_coins_empty_df(mocker):
    view_path = "gamestonk_terminal.cryptocurrency.discovery.coinmarketcap_view"

    # MOCK GET_SEARCH_RESULTS
    mocker.patch(
        target=f"{view_path}.coinmarketcap_model.get_cmc_top_n",
        return_value=pd.DataFrame(),
    )

    coinmarketcap_view.display_cmc_top_coins()
