xarray-stac
============

Tool to create data cubes using data retrieved from STAC catalogs.

Usage
------

To exemplify the use of xarray-stac, the STAC catalog of the Brazil Data Cube project will be used as a basis. The first step is made with the search of some data in the catalog:

.. code-block:: python

    import stac.py

    # getting data
    bdc_stac_service = stac.STAC('http://brazildatacube.dpi.inpe.br/stac/')
    collection = bdc_stac_service.collection('S2_10_16D_STK-1')
    items = collection.get_items(filter={'bbox':'-61, 2.8, -60, 1.8', 'datetime':'2018-08-01/2019-07-31'})

Once with the data, you can use the ``cube_from_stac_collection`` function to create a data cube with the items collections that comes from the STAC catalog:

.. code-block:: python

    from xarray_stac.cube import cube_from_stac_collection
    cube = cube_from_stac_collection(items['features'][0:2], ['NDVI', 'band08'])

.. NOTE::

    The first parameter represents the list of features and the second the list of bands that need to be in the dimensions of the cube that is being generated
