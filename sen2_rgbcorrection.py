# import libraries
import os
from zipfile import ZipFile

# define variables
folder = "/Users/williamray/Downloads/Biocarbon_python_test/S2A_MSIL2A_20180901T105621_N0208_R094_T31UDQ_20180901T162709.SAFE/GRANULE/L2A_T31UDQ_A016679_20180901T105939/IMG_DATA/R10m/"
R = folder+"T31UDQ_20180901T105621_B04_10m.jp2"
G = folder+"T31UDQ_20180901T105621_B03_10m.jp2"
B = folder+"T31UDQ_20180901T105621_B02_10m.jp2"
rgbimage = "rgb.tif"
rgb_color_corrected = "rgb_corrected.tif"

# unzip sentinel 2 zip file
sen2zip = ZipFile('S2A_MSIL2A_20180901T105621_N0208_R094_T31UDQ_20180901T162709.zip', 'r')
sen2zip.extractall('')

# stack individual bands into an RGB image
os.system("gdal_merge.py -n 0 -a_nodata 0 -separate -of GTiff -o %s %s %s %s" % (rgbimage, R, G, B))

# color correct the RGB image using rio color https://github.com/mapbox/rio-color
os.system("rio color -d uint16 -j 4 %s %s gamma G 1.1 gamma B 1.2 sigmoidal RGB 6 0.5 saturation 1.15" % (rgbimage, rgb_color_corrected))
