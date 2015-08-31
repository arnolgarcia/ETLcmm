__author__ = 'Arnol'

import ogr, gdal
import numpy as np
import os

# Parametros
dir = 'C:/Users/Arnol/Desktop/puntos_poligonos_cmm/'
polygon_fn = 'poligono_test.shp'
input_file = dir + polygon_fn
temp_file = dir + 'temp.tif'
output_shp = dir + 'points.shp'
pixel_size = 10


# Open the data source and read in the extent
source_ds = ogr.Open(input_file)
source_layer = source_ds.GetLayer()
x_min, x_max, y_min, y_max = source_layer.GetExtent()


# Create the destination data source
x_res = int((x_max - x_min) / pixel_size)
y_res = int((y_max - y_min) / pixel_size)
target_ds = gdal.GetDriverByName('GTiff').Create(temp_file, x_res, y_res, gdal.GDT_Byte)
target_ds.SetGeoTransform((x_min, pixel_size, 0, y_max, 0, -pixel_size))
band = target_ds.GetRasterBand(1)
band.SetNoDataValue(255)

# Rasterize
gdal.RasterizeLayer(target_ds, [1], source_layer, burn_values=[1])

# Read as array
array = band.ReadAsArray()

raster = gdal.Open(temp_file)
geotransform = raster.GetGeoTransform()

# Convert array to point coordinates
count = 0
roadList = np.where(array == 1)
multipoint = ogr.Geometry(ogr.wkbMultiPoint)
for indexY in roadList[0]:
    indexX = roadList[1][count]
    geotransform = raster.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    Xcoord = originX+pixelWidth*(indexX+0.5)
    Ycoord = originY+pixelHeight*(indexY+0.5)
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(Xcoord, Ycoord)
    multipoint.AddGeometry(point)
    count += 1

# Write point coordinates to Shapefile
shpDriver = ogr.GetDriverByName("ESRI Shapefile")
if os.path.exists(output_shp):
    shpDriver.DeleteDataSource(output_shp)
outDataSource = shpDriver.CreateDataSource(output_shp)
outLayer = outDataSource.CreateLayer(output_shp, geom_type=ogr.wkbMultiPoint)
featureDefn = outLayer.GetLayerDefn()
outFeature = ogr.Feature(featureDefn)
outFeature.SetGeometry(multipoint)
outLayer.CreateFeature(outFeature)

# Remove temporary files
#os.remove('temp.tif')