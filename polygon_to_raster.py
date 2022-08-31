import pandas as pd
import geopandas as gpd
from geocube.api.core import make_geocube
from geocube.rasterize import rasterize_image
from functools import partial
from rasterio.enums import MergeAlg


def polygonsToRaster():
    # Read California Census Polygon Shapefile
    cal_census = gpd.read_file('shps/california_census/census_pops.shp')
    cal_census = cal_census.rename(columns={'POP20': 'pops'})

    # Reprojecting to 3857 coordinate system
    cal_census = cal_census.to_crs('EPSG:3857')
    
    # Using GeoCube to rasterize the Vector
    cal_census_raster = make_geocube(
        vector_data=cal_census,
        measurements=["pops"],
        resolution=(-500, 500),
        fill = 0
    )
    
    # Save raster census raster
    cal_census_raster.rio.to_raster('rasters/cal_census.tiff')

def pointsToRaster():
    # Read UK Accidents Point Shapefile
    uk_accidents = pd.read_csv('csvs/uk_accidents_2005_to_2014.csv')

    # Convert Long Lat into numeric type
    uk_accidents['Longitude'] = pd.to_numeric(uk_accidents['Longitude'])
    uk_accidents['Latitude'] = pd.to_numeric(uk_accidents['Latitude'])

    # Convert Long Lat into Point Geometry
    uk_accidents = gpd.GeoDataFrame(geometry = gpd.points_from_xy(x=uk_accidents['Longitude'], y=uk_accidents['Latitude']))
    uk_accidents = uk_accidents.set_crs('EPSG:4326')

    # Reprojecting to 3857 coordinate system
    uk_accidents = uk_accidents.to_crs('EPSG:3857')
    uk_accidents['value'] = 1
    uk_accidents = uk_accidents[uk_accidents.is_valid]
    uk_accidents = uk_accidents[~uk_accidents.is_empty]
    
    # Using GeoCube to rasterize the Vector
    uk_accidents_raster = make_geocube(
        vector_data=uk_accidents,
        measurements=["value"],
        resolution=(-500, 500),
        rasterize_function=partial(rasterize_image, merge_alg=MergeAlg.add), 
        fill = 0
    )

    # save uk_accidents raster
    uk_accidents_raster.rio.to_raster('rasters/uk_accidents.tiff')

if __name__ == '__main__':
    polygonsToRaster()
    pointsToRaster()
    
