def rio_magdalena_tebsa_bquilla(l: float, limit: float = 0.05) -> float:
    """
    Predict the water level for the TEBSA station in Barranquilla on the Magdalena River.

    Parameters
    ----------
    l : float
        The reference water level.
    limit : float, optional
        Minimum limit for the predicted level, by default 0.05.

    Returns
    -------
    float
        The predicted water level.
    """
    predicted_l = -0.550 + 0.287 * l
    if predicted_l > limit:
        return predicted_l
    else:
        return limit


def rio_magdalena_sitio_nuevo(l: float, limit: float = 0.230) -> float:
    """
    Predict the water level for the Sitio Nuevo station on the Magdalena River.

    Parameters
    ----------
    l : float
        The reference water level.
    limit : float, optional
        Minimum limit for the predicted level, by default 0.230.

    Returns
    -------
    float
        The predicted water level.
    """
    predicted_l = -0.795 + 0.456 * l
    if predicted_l > limit:
        return predicted_l
    else:
        return limit


def canal_dique_villa_rosa(l: float, limit: float = 0.10) -> float:
    """
    Predict the water level for the Villa Rosa station on the Canal del Dique.

    Parameters
    ----------
    l : float
        The reference water level.
    limit : float, optional
        Minimum limit for the predicted level, by default 0.10.

    Returns
    -------
    float
        The predicted water level.
    """
    predicted_l = -0.18 * l + l
    if predicted_l > limit:
        return predicted_l
    else:
        return limit
