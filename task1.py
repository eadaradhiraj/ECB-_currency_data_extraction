import pandas as pd
import requests
from bs4 import BeautifulSoup
from typing import Optional


def convert_data_to_df(url: str) -> pd.DataFrame:
    try:
        _request = requests.get(url)
        if _request.status_code != 200:
            print(f"Error status code: {_request.status_code}")
            return pd.DataFrame([], columns=["TIME_PERIOD", "OBS_VALUE"])
        _soup = BeautifulSoup(_request.content, features="html.parser").find_all(
            "generic:obs"
        )
        _dict_list = [
            {
                "generic:obsdimension": obs.find("generic:obsdimension").get("value"),
                "generic:obsvalue": obs.find("generic:obsvalue").get("value"),
            }
            for obs in _soup
        ]
    except Exception as err:
        print(err)
        return pd.DataFrame([], columns=["TIME_PERIOD", "OBS_VALUE"])
    _columns = {"generic:obsdimension": "TIME_PERIOD", "generic:obsvalue": "OBS_VALUE"}
    return (
        pd.DataFrame(_dict_list)
        .astype({"generic:obsdimension": "object", "generic:obsvalue": "float64"})
        .rename(columns=_columns)
    )


def get_exchange_rate(source: str, target: str = "EUR") -> pd.DataFrame:
    return convert_data_to_df(
        f"https://sdw-wsrest.ecb.europa.eu/service/data/EXR/M.{source}.{target}.SP00.A?detail=dataonly"
    )


def get_raw_data(identifier: str) -> pd.DataFrame:
    return convert_data_to_df(
        f"https://sdw-wsrest.ecb.europa.eu/service/data/BP6/{identifier}?detail=dataonly"
    )


def get_data(identifier: str, target_currency: Optional[str] = None) -> pd.DataFrame:
    raw_data = get_raw_data(identifier=identifier)
    if not target_currency:
        return raw_data
    exchange_rate = get_exchange_rate(
        source=target_currency, target=identifier.split(".")[12]
    )
    raw_data = raw_data.join(
        exchange_rate.set_index("TIME_PERIOD"),
        on="TIME_PERIOD",
        lsuffix="_l",
        rsuffix="_r",
    )
    raw_data["OBS_VALUE"] = raw_data["OBS_VALUE_r"] * raw_data["OBS_VALUE_l"]
    return raw_data.drop(columns=["OBS_VALUE_r", "OBS_VALUE_l"])


if __name__ == "__main__":
    import os

    _cwd = os.getcwd()

    get_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N", "GBP").to_csv(
        os.path.join(_cwd, "gbp_test_data.csv"), index=False
    )
    get_raw_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N").to_csv(
        os.path.join(_cwd, "gbp_test_raw_data.csv"), index=False
    )
    get_exchange_rate("GBP").to_csv(
        os.path.join(_cwd, "gbp_test_exchange_rate.csv"), index=False
    )
    get_exchange_rate("NOK").to_csv(
        os.path.join(_cwd, "nok_test_exchange_rate.csv"), index=False
    )

