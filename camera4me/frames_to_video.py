import os 
from pathlib import Path

import argparse

import cv2 as cv
import numpy as np
import glob

import subprocess

import logging
LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s')
logging.basicConfig( level=logging.DEBUG, format=LOG_FORMAT )

LOGGER = logging.getLogger( __name__ )

FRAMES_FOLDER = "/data/"
VIDEO_FOLDER = "/data/frames/"        # Store video on parent-folder

# VIDEO CONVERSION
VIDEO_FILE_NAME = "parking-space-masked.avi"
MP4_NAME = "parking-space-masked.mp4"
WEBM_NAME = "parking-space-masked.webm"

FFMPEG_COMMAND = f"ffmpeg -y -i {VIDEO_FOLDER+VIDEO_FILE_NAME} -c:v libx264 -preset slow -crf 19 -c:a copy {VIDEO_FOLDER+MP4_NAME}"
FFMPEG_COMMAND_SIMPLE = "ffmpeg -y -i /data/frames/parking-space-masked.avi /data/frames/parking-space-masked.mp4"

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
    all_counter = len( glob.glob( myfolder ) )
    LOGGER.debug( f"Number of Files in Directory ... {all_counter}" )

    jpg_counter = len( glob.glob( myfolder + "/*.jpg" ) )
    LOGGER.debug( f"Number of JPG Files in Directory ... {jpg_counter}" )

    img_array = []
    for filename in glob.glob( myfolder + "/*.jpg" ): #  myfolder + "/**/*.jpg" ):
        LOGGER.debug( f"Handling ... {filename}" )
        
        img = cv.imread(filename)
        
        img_array.append( img )

    LOGGER.debug("Finished Reading Masked Frames")
    
    return img_array

def convert_images_to_video( images_all, name, size ):
    #out = cv.VideoWriter( name, cv.VideoWriter_fourcc(*'DIVX'), 15, size)
    #out = cv.VideoWriter( name, cv.VideoWriter_fourcc(*'mp4v'), 20.0, size)
    out = cv.VideoWriter( name, cv.VideoWriter_fourcc(*'vp80'), 10, size)

    LOGGER.debug("Filling Video")

    counter = 1
    for img in images_all:
        LOGGER.debug(f"Wrote {counter}")
        out.write(img)

        counter = counter + 1

    LOGGER.debug("Finished Filling")
    out.release()

def check_if_directory_exists( p_in ):
    #os.path.exists()
    p = Path(p_in)

    print("Out")
    if p.is_dir():
        print("In")
        [print(x) for x in p.iterdir() if x.is_dir()]

    return p.is_dir()

def convert_avi_to_mp4(avi_file_path, ouput_mp4_name):
    try:
        #res = os.popen( FFMPEG_COMMAND )
        res = os.popen( FFMPEG_COMMAND_SIMPLE )
    except Exception as ex:
        LOGGER.error(f"-->{ex}")

    return
       
def video_main():
    """ Main """    
    LOGGER.info( "*********************************************************" )
    LOGGER.info( "** Video-Maker ver3.0 : Turn Image Sequence into Video **" )
    LOGGER.info( "*********************************************************" )

    parser = argparse.ArgumentParser( description='Arguments for Video-Maker Tool' )

    parser.add_argument( '--frames_folder', required=False, type=str, help='Read Frames from Folder', default=None )
    parser.add_argument( '--video_folder', required=False, type=str, help='Save Video into Folder', default=None )
    
    # Location
    #parser.add_argument( '--host', required=True, type=str, help='RabbitMQ Server IP-Address')
    #parser.add_argument( '--port', required=False, type=int, help='RabbitMQ Server AMQP-Port', default=5672 )

    args = parser.parse_args()

    if args.frames_folder is None:
        LOGGER.debug("No Frames-Folder is Specified ... using Default !")

        # ==> Use Default Folders
        LOGGER.debug( f"Is +Default+ Frames Folder OK : {FRAMES_FOLDER} --> {check_if_directory_exists( FRAMES_FOLDER )}" )
        #LOGGER.debug( f"Check Folder Exists : {VIDEO_FOLDER}  --> {check_if_directory_exists( VIDEO_FOLDER )}" )

        #img_array = read_images_from_folder( FRAMES_FOLDER )
    else:
        LOGGER.debug(f"Frames-Folder is User-Specified ... {args.frames_folder}")

        # ==> User-specified Folder
        LOGGER.debug( f"Is +User Specified+ Frames-Folder OK : {args.frames_folder} --> {check_if_directory_exists(args.frames_folder)}" )
        #LOGGER.debug( f"Check Folder Exists : {VIDEO_FOLDER}  --> {check_if_directory_exists( VIDEO_FOLDER )}" )

        #img_array = read_images_from_folder( FRAMES_FOLDER )
        
    return

    
    img = img_array[0]
    [height, width, layers] = img.shape
    size = (width, height)

    #convert_images_to_video( img_array, VIDEO_FOLDER + VIDEO_FILE_NAME, size )
    #convert_images_to_video( img_array, VIDEO_FOLDER + MP4_NAME, size )
    convert_images_to_video( img_array, VIDEO_FOLDER + WEBM_NAME, size)

    LOGGER.debug( img_array )
    
    #convert_avi_to_mp4("avi_file", "mp4_file")
    
    return