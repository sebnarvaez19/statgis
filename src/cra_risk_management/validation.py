import datetime
import zoneinfo

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes

tz: zoneinfo.ZoneInfo = zoneinfo.ZoneInfo(key="America/Bogota")
month_to_delete: int = 2
day_to_delete: int = 29


def check_year(year: int | None) -> int:
    """Check the year."""
    if year is None:
        year: int = datetime.datetime.now(tz=tz).year
    return year


def check_df_integrity(df: pd.DataFrame) -> pd.DataFrame:
    """Check the integrity of the dataset."""
    if not ("datetime" in df.columns or "datum" in df.columns):
        raise ValueError("'datetime' and 'datum' columns weren't encountered")
    return df


def remove_feb_29th(df: pd.DataFrame) -> pd.DataFrame:
    """Remove the 29th of February from the dataset."""
    return df.loc[
        ~(
            (df["datetime"].dt.month == month_to_delete)
            & (df["datetime"].dt.day == day_to_delete)
        )
    ].copy()


def check_ax(ax: Axes | None) -> Axes:
    """Check the axes."""
    if ax is None:
        ax: Axes = plt.subplots()[1]
    return ax
