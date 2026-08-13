def rio_magdalena_tebsa_bquilla(l: float, limit: float = 0.05) -> float:
    predicted_l = -0.550 + 0.287 * l
    if predicted_l > limit:
        return predicted_l
    else:
        return limit
    

def rio_magdalena_sitio_nuevo(l: float, limit: float = 0.500) -> float:
    predicted_l = -0.795 + 0.456 * l
    if predicted_l > limit:
        return predicted_l
    else:
        return limit


def canal_dique_villa_rosa(l: float, limit: float = 3.00) -> float:
    predicted_l = -0.052 * l + l
    if predicted_l > limit:
        return predicted_l
    else:
        return limit