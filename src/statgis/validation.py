import datetime

import pandas as pd


def check_year(year: int | None) -> int:
    """
    Check the year.
    """
    if year is None:
        year = datetime.datetime.now().year
    return year


def check_df_integrity(df: pd.DataFrame) -> pd.DataFrame:
    """
    Check the integrity of the dataset.
    """
    if not ("datetime" in df.columns or "datum" in df.columns):
        raise ValueError("'datetime' and 'datum' columns weren't encountered")
    return df


def remove_feb_29th(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove the 29th of February from the dataset.
    """
    return df.loc[~((df["datetime"].dt.month == 2) & (df["datetime"].dt.day == 29))].copy()