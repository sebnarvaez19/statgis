from pathlib import Path

import geopandas as gpd
from prepare_wfs_data import prepare_data


def process_ororatech_data(file_path: Path | str) -> gpd.GeoDataFrame:
    """Prepare OroraTech Wildfire Solutions data.

    Parameters
    ----------
    file_path: Path | str
        Path to file to process.

    Returns
    -------
    gpd.GeodataFrame
        Data processed.

    """
    gdf = gpd.read_file(file_path)
    return prepare_data(gdf)
