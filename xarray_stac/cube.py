import os
import warnings
from urllib.parse import urlparse

import pandas as pd
import xarray as xr


def _href_to_path(href, basepath):
    url = urlparse(href)
    return os.path.normpath(basepath + url.path)


def cube_from_stac_collection(collection_feature: list, data_variables: list, base_path = None) -> xr.Dataset:
    """Create a datacube (One variable) from a STAC-Collection
    Args:
        collectionfeature (collection_feature): Feature Collection from STAC
        data_variables (list): string list with variables to include in datacube's data dimension
        base_path (str): File System path. Use when you have data product and STAC with same path, changing only the base path
    Example (Using Brazil Data Cube's service):
        >> bdc_stac_service = stac.STAC('http://brazildatacube.dpi.inpe.br/stac/')
        >> collection = bdc_stac_service.collection('S2_10_16D_STK-1')
        >> items = collection.get_items(filter={'bbox':'-61, 2.8, -60, 1.8', 'datetime':'2018-08-01/2019-07-31'})
        >> cube_from_stac_collection(items['features'][0:2], ['NDVI', 'band08'])
    """

    if not isinstance(collection_feature, list):
        warnings.warn("A list is expected, trying to execute by converting the entry to a list")
        collection_feature = [collection_feature]

    def create_timeindex(timeseries_index):
        """Convert list of string time into pandas.DatetimeIndex
        Args:
            timeseries_index (list): List of string
        """
        return pd.DatetimeIndex(
            [pd.Timestamp(times) for times in timeseries_index]
        )

    # extract timeseries index
    time_dimension = xr.Variable('time', create_timeindex(
        [feature['properties']['datetime'] for feature in collection_feature]
    ))

    cube = xr.Dataset()
    for data_variable in data_variables:
        data_list = []
        for feature in collection_feature:
            href = feature['assets'][data_variable]['href']
            if base_path:
                href = _href_to_path(href, base_path)
            data_list.append(xr.open_rasterio(href))
        cube[data_variable] = xr.concat(data_list, dim=time_dimension)
    return cube
