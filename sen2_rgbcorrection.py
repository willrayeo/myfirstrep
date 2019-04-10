# import libraries
import os
from zipfile import ZipFile

class Sen2colorcorrection():
    """
    Class that collects methods of CNNClassifier class

    class attributes:
    zipfile = the sentinel 2 zipfile downloaded from openhub. Can sit in same directory\
    as the script, otherwise specify full file pathself.

    """

    # Initializer / Instance Attributes
    def __init__(self,
                 zipfile,
                 rgb_color_corrected,
                 R = "*.SAFE/GRANULE/*/IMG_DATA/*_B04.jp2",
                 G = "*.SAFE/GRANULE/*/IMG_DATA/*_B03.jp2",
                 B = "*.SAFE/GRANULE/*/IMG_DATA/*_B02.jp2",
                 rgbimage = "rgb.tif"):
        self.unzip(zipfile)
        ok = self.stack(rgbimage, R, G, B)
        self.correct(rgbimage, rgb_color_corrected)

    # unzip sentinel 2 zip file

    def unzip(self, zipfile):
        sen2zip = ZipFile(zipfile, 'r')
        sen2zip.extractall('')

    # stack individual bands into an RGB image

    def stack(self, rgbimage, R, G, B):
        success = os.system("gdal_merge.py -n 0 -a_nodata 0 -separate -of GTiff -o %s %s %s %s" % (rgbimage, R, G, B))
        return success
    # color correct the RGB image using rio color https://github.com/mapbox/rio-color
    def correct(self, rgbimage, rgb_color_corrected):
        success = os.system("rio color -d uint16 -j 4 %s %s gamma G 1.1 gamma B 1.2 sigmoidal RGB 6 0.5 saturation 1.15" % (rgbimage, rgb_color_corrected))
        print("your image has been corrected")
        return success

# Variables as strings
#zipfile = '/home/kore-dev/Documents/objects/L1C_T18TWL_A016310_20180806T154402.zip'
#folder = "*.SAFE/GRANULE/*/IMG_DATA/"
#R = folder+"*_B04.jp2"
#G = folder+"*_B03.jp2"
#B = folder+"*_B02.jp2"


Sen2colorcorrection('L1C_T18TWL_A016310_20180806T154402.zip', 'mycorrectedimg.tif')
