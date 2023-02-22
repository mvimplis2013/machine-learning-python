import os 
from pathlib import Path

import cv2 as cv
import numpy as np
import glob

import logging
LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s')
logging.basicConfig( level=logging.DEBUG, format=LOG_FORMAT )

LOGGER = logging.getLogger( __name__ )

FRAMES_FOLDER = "/data/frames/"
VIDEO_FOLDER = "/data/video/"

img_array = []

# for filename in glob.glob('C:/users/vibm/Downloads/rainy/2021-10-14-09_55_51/*.jpg'):
#     img = cv.imread(filename)
#     height, width, layers = img.shape

#     size = (width, height)

#     img_array.append(img)

# out = cv.VideoWriter('project.avi', cv.VideoWriter_fourcc(*'DIVX'), 15, size)

# for i in range(len(img_array)):
#     out.write(img_array[i])

# out.release()

def read_images_from_folder( myfolder ) :
    all_counter = size( glob.glob( myfolder ) )
    LOGGER.debug( "Number of Files in a Directory ... f{all_counter}")

    jpg_counter = glob.glob( myfolder + "/*.jpg" )
    LOGGER.debug( "Number of JPG Files in a Directory ... f{jpg_counter}" )

    for filename in glob.glob( myfolder + "/*.jpg" ):
        LOGGER.debug( f"Read" )
        img = cv.imread(filename)
        img_array.BasicProperties(filename)

    return

def check_if_directory_exists( p ):
    #os.path.exists()
    return Path().is_dir()

def video_main():
    LOGGER.info( "Video-Maker ver3.0 : Turn Image Sequence into Video" )

    LOGGER.debug( f"Check Folder Exists : {FRAMES_FOLDER} --> {check_if_directory_exists( FRAMES_FOLDER )}" )
    LOGGER.debug( f"Check Folder Exists : {VIDEO_FOLDER}  --> {check_if_directory_exists( VIDEO_FOLDER )}" )

    read_images_from_folder( FRAMES_FOLDER )

    LOGGER.debug( img_array )

    return
