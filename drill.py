def mutate_1d_cube(collectionfeature, datavar):
    """Create a datacube with '1D' (One variable) from BDC-STAC items
    
    Args:
        collectionfeature (list): Feature Collection from BDC-STAC
        datavar (str): string with variable name
        
    Example:
        >> bdc_stac_service = stac.STAC('http://brazildatacube.dpi.inpe.br/stac/')
        
        >> collection = bdc_stac_service.collection('S2_10_16D_STK-1')
        
        >> items = collection.get_items(filter={'bbox':'-61, 2.8, -60, 1.8', 'datetime':'2018-08-01/2019-07-31'})
        
        >> mutate_1d_cube(items['features'], 'NDVI')
    """
        
    def create_timeindex(timeseries_index):
        """Convert list of string time into pandas.DatetimeIndex
        Args:
            timeseries_index (list): List of string
        """
        return pd.DatetimeIndex(
            [pd.Timestamp(times) for times in timeseries_index]
        )
        
    timeseries_index = []
    cube_layer = xr.Dataset()
    
    # extract timeseries index
    time_dimension = xr.Variable('time', create_timeindex(
        [feature['properties']['datetime'] for feature in collectionfeature]
    ))
        
    return xr.concat([
        xr.open_rasterio(feature['assets'][datavar]['href']) for feature in collectionfeature
    ], dim = time_dimension)
