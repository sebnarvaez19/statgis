from collections.abc import Sequence

import pandas as pd
import requests

from cra_risk_management.constants import API_URL, DEFAULT_PERCENTILES
from cra_risk_management.validation import (
    check_df_integrity,
    check_year,
    remove_feb_29th,
)


def load_dataset(station_id: int) -> pd.DataFrame:
    """
    Load the dataset for a given station ID.

    Args:
        station_id (int): The ID of the station.

    Returns:
        pd.DataFrame: The dataset for the given station ID.
    """
    url = f"{API_URL}/hidrometorological/datasets/{station_id}"
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
    df = df.copy()
    df = check_df_integrity(df)
    df = df.loc[
        (df["datetime"] >= f"{year}-01-01") & (df["datetime"] <= f"{year}-12-31")
    ].copy()
    df = remove_feb_29th(df)
    return df


def get_probability_dataset(
    df: pd.DataFrame,
    year: int | None = None,
    percentiles: Sequence[float] = DEFAULT_PERCENTILES,
) -> pd.DataFrame:
    """
    Get the probability dataset for a given year.

    Args:
        df (pd.DataFrame): The dataset for the given station ID.
        year (int | None, optional): The year to get the dataset for. Defaults to None.
        percentiles (Sequence[float], optional): The percentiles to get the dataset for. Defaults to DEFAULT_PERCENTILES.

    Returns:
        pd.DataFrame: The probability dataset for the given year.
    """
    year = check_year(year)
    df = df.copy()
    df = check_df_integrity(df)
    df["month"], df["day"] = df["datetime"].dt.month, df["datetime"].dt.day
    df = df.loc[~((df["month"] == 2) & (df["day"] == 29))]
    df = (
        df.groupby(["month", "day"])["datum"]
        .quantile(percentiles)
        .unstack()
        .reset_index()
    )
    df = df.drop(columns=["month", "day"])
    idx = pd.date_range(f"{year}-01-01", f"{year}-12-31", freq="D")
    if len(idx) > 365:
        idx = idx.drop([f"{year}-02-29"])
    return df.set_index(idx)
