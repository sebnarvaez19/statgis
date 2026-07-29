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
