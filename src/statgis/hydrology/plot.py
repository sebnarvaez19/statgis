import pandas as pd
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
