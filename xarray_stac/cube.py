import warnings

import xarray as xr
import pandas as pd


def cube_from_stac_collection(collection_feature: list, data_variables: list) -> xr.Dataset:
    """Create a datacube (One variable) from a STAC-Collection

    Args:
        collectionfeature (collection_feature): Feature Collection from STAC
        data_variables (list): string list with variables to include in datacube's data dimension

    Example (Using Brazil Data Cube's service):
        >> bdc_stac_service = stac.STAC('http://brazildatacube.dpi.inpe.br/stac/')

        >> collection = bdc_stac_service.collection('S2_10_16D_STK-1')

        >> items = collection.get_items(filter={'bbox':'-61, 2.8, -60, 1.8', 'datetime':'2018-08-01/2019-07-31'})

        >> mutate_1d_cube(items['features'], 'NDVI')
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
        cube[data_variable] = xr.concat([
            xr.open_rasterio(feature['assets'][data_variable]['href']) for feature in collection_feature
        ], dim=time_dimension)
    return cube
