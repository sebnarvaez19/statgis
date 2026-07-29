import requests
from typing import Sequence

import pandas as pd
from statgis.constants import API_URL, DEFAULT_PERCENTILES
from statgis.validation import check_year, check_df_integrity, remove_feb_29th


def load_dataset(station_id: int) -> pd.DataFrame:
    """
    Load the dataset for a given station ID.

    Args:
        station_id (int): The ID of the station.

    Returns:
        pd.DataFrame: The dataset for the given station ID.
    """
    url = f"{API_URL}/datasets/{station_id}"
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(response.text)
    df = pd.DataFrame.from_records(response.json()).set_index("id")
    df.index.name = None
    df["datetime"] = pd.to_datetime(df["datetime"])
    return df


def get_dataset_year(df: pd.DataFrame, year: int | None = None) -> pd.DataFrame:
    """
    Get the dataset for a given year.

    Args:
        df (pd.DataFrame): The dataset for the given station ID.
        year (int | None, optional): The year to get the dataset for. Defaults to None.

    Returns:
        pd.DataFrame: The dataset for the given year.
    """
    year = check_year(year)
    df = check_df_integrity(df)
    df = df.loc[(df["datetime"] >= f"{year}-01-01") & (df["datetime"] <= f"{year}-12-31")].copy()
    df = remove_feb_29th(df)
    return df
