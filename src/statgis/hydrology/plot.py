import pandas as pd
import numpy as np
from matplotlib.axes import Axes

from statgis import constants, validation
from statgis.hydrology import data
from statgis.hydrology import predict


def time_stripe(df: pd.DataFrame, year: int | None = None, ax: Axes | None = None) -> Axes:
    """
    Plot the time stripe of the dataset.
    
    Parameters
    ----------
    df : pd.DataFrame
        The dataset.
    year : int | None, optional
        The year to plot, by default None.
    ax : Axes | None, optional
        The axes to plot on, by default None.
    
    Returns
    -------
    Axes
        The axes with the time stripe plotted.
    """
    ax = validation.check_ax(ax)
    df_prob = data.get_probability_dataset(df, year=year)
    ax.fill_between(df_prob.index, df_prob[0.0], df_prob[1.0], facecolor="C0", alpha=0.3)
    ax.fill_between(df_prob.index, df_prob[0.1], df_prob[0.9], facecolor="C0", alpha=0.3)
    ax.fill_between(df_prob.index, df_prob[0.25], df_prob[0.75], facecolor="C0", alpha=0.3)
    ax.plot(df_prob.index, df_prob[0.5], color="C0")
    ax.set(xlim=[df_prob.index[0], df_prob.index[-1]])
    ax.text(x=df_prob.index[-1], y=df_prob[0.0].iloc[-1], s="Min", ha="right", va="center", fontsize="small")
    ax.text(x=df_prob.index[-1], y=df_prob[0.1].iloc[-1], s="10%", ha="right", va="center", fontsize="small")
    ax.text(x=df_prob.index[-1], y=df_prob[0.25].iloc[-1], s="25%", ha="right", va="center", fontsize="small")
    ax.text(x=df_prob.index[-1], y=df_prob[0.5].iloc[-1], s="50%", ha="right", va="center", fontsize="small")
    ax.text(x=df_prob.index[-1], y=df_prob[0.75].iloc[-1], s="75%", ha="right", va="center", fontsize="small")
    ax.text(x=df_prob.index[-1], y=df_prob[0.9].iloc[-1], s="90%", ha="right", va="center", fontsize="small")
    ax.text(x=df_prob.index[-1], y=df_prob[1.0].iloc[-1], s="Max", ha="right", va="center", fontsize="small")
    return ax


def plot_year(df_year: pd.DataFrame, ax: Axes | None = None) -> Axes:
    """
    Plot the year.

    Parameters
    ----------
    df_year : pd.DataFrame
        The dataset.
    ax : Axes | None, optional
        The axes to plot on, by default None.

    Returns
    -------
    Axes
        The axes with the year plotted.
    """
    ax = validation.check_ax(ax)
    ax.plot(df_year["datetime"], df_year["datum"], color="black")
    return ax


def magdalena_river_backwater(ax: Axes | None = None) -> Axes:
    """
    Plot the backwater curve of the Magdalena River.

    Parameters
    ----------
    ax : Axes | None, optional
        The axes to plot on, by default None.

    Returns
    -------
    Axes
        The axes with the backwater curve plotted.
    """
    ax = validation.check_ax(ax)
    df = data.load_dataset(29037020)
    x = pd.DataFrame({
        109.5: df.quantile(constants.DEFAULT_PERCENTILES)["datum"],
        35.71: df.quantile(constants.DEFAULT_PERCENTILES)["datum"].map(predict.rio_magdalena_sitio_nuevo),
        20.00: df.quantile(constants.DEFAULT_PERCENTILES)["datum"].map(predict.rio_magdalena_tebsa_bquilla),
        0.000: df.quantile(constants.DEFAULT_PERCENTILES)["datum"].map(lambda x: 0),
    }).T
    t = pd.Series([
        df.sort_values("datetime").iloc[-1]["datum"],
        predict.rio_magdalena_sitio_nuevo(df.sort_values("datetime").iloc[-1]["datum"]),
        predict.rio_magdalena_tebsa_bquilla(df.sort_values("datetime").iloc[-1]["datum"]),
        0,
    ])
    for name, distance in constants.BOCATOMAS_RÍO_MAGDALENA:
        ax.axvline(x=distance, color="gray", linestyle="--", linewidth=1)
        ax.text(x=distance, y=6, s=name, rotation=90, ha="right", va="center", fontsize="small")
    x_stations = list(map(lambda x: x[1], constants.ESTACIONES_RÍO_MAGDALENA))
    ax.scatter(
        x=x_stations,
        y=np.full_like(x_stations, 0.98, dtype=float),
        c="#BA8E23",
        transform=ax.get_xaxis_transform(),
        marker="v",
        label="Estaciones IDEAM",
    )
    for name, distance in constants.ESTACIONES_RÍO_MAGDALENA:
        ax.text(x=distance, y=0.98, s=name, ha="center", va="bottom", fontsize="small", transform=ax.get_xaxis_transform())
    ax.fill_between(x.index, x[0.0], x[1.0], facecolor="C0", alpha=0.3, label="Variabilidad nivel")
    ax.fill_between(x.index, x[0.1], x[0.9], facecolor="C0", alpha=0.3)
    ax.fill_between(x.index, x[0.25], x[0.75], facecolor="C0", alpha=0.3)
    ax.plot(x.index, x[0.5], color="C0")
    ax.plot(x.index, t, color="black", label="Nivel actual")
    ax.text(x=109.5, y=x[0.0].iloc[0], s="Min", ha="left", va="center", fontsize="small")
    ax.text(x=109.5, y=x[0.1].iloc[0], s="10%", ha="left", va="center", fontsize="small")
    ax.text(x=109.5, y=x[0.25].iloc[0], s="25%", ha="left", va="center", fontsize="small")
    ax.text(x=109.5, y=x[0.5].iloc[0], s="50%", ha="left", va="center", fontsize="small")
    ax.text(x=109.5, y=x[0.75].iloc[0], s="75%", ha="left", va="center", fontsize="small")
    ax.text(x=109.5, y=x[0.9].iloc[0], s="90%", ha="left", va="center", fontsize="small")
    ax.text(x=109.5, y=x[1.0].iloc[0], s="Max", ha="left", va="center", fontsize="small")
    ax.xaxis.set_inverted(True)
    return ax