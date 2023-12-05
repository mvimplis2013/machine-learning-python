# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from configparser import ConfigParser
from datetime import datetime
from time import sleep, ctime

import cv2
import os, sys
#from google_client_upload_frames import main_google_drive_client

MONITORING_DURATION_MINS = 600
 
# Wait SECs for Next Snapshot
SLEEP_BETWEEN_SNAPSHOTS = 3

import logging
LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s')
logging.basicConfig( level=logging.DEBUG, format=LOG_FORMAT )

LOGGER = logging.getLogger( __name__ )

# Read the Camera Video Output
def open_rtsp_stream(ip, username, password):
    global MONITORING_DURATION_MINS
    global SLEEP_BETWEEN_SNAPSHOTS

    # Make folder to store frames
    # Date_Minute
    my_datetime = datetime.today().strftime('%Y-%m-%d-%H_%M_%S')
    
    # !!!!!!! Where to store frames !!!!!!
    new_path = f'%svideo/frames/%s' % (OUTPUT_DIR , my_datetime)
    LOGGER.debug( f"Store Frames in ... {new_path}" )

    if not os.path.exists(new_path):
        os.makedirs(new_path)

    # Grab first frame
    vcap = cv2.VideoCapture("rtsp://" + username + ":" + password + "@" + ip)
    
    # Check Success
    if not vcap.isOpened():
        #raise Exception("Could Not Open Video Device")
        LOGGER.error(f"!!! Could Not Open Video Device ... {'rtsp://' + username + ':' + password + '@' + ip} !!!")
        return

    # Restrict FIFO queue to a single image 
    
    vcap.set(CAP_PROP_BUFFERSIZE, 1)

    #ret, frame = vcap.read()
    #sleep( SLEEP_BETWEEN_SNAPSHOTS )

    #if not ret:
        #raise Exception("Cannot Receive Frame (Stream End ?)")
    #    LOGGER.error(f"*** Cannot Receive Frame (Stream End ?) ... {'rtsp://' + username + ':' + password + '@' + ip} ***")
    #    return

    current_dt = datetime.now()
    #previous_dt = datetime.now()
    start_time = current_dt.timestamp()
    
    monitoring_minutes = (MONITORING_DURATION_MINS * 60)
    LOGGER.debug(f"Ready to Start Capturing for Time-Period (in Secs) = {monitoring_minutes} ... START = {ctime()}")

    #counter = 0
    while True:
        # Start frames capturing at ...
        time_passed = datetime.now().timestamp() - start_time

        if time_passed > monitoring_minutes:
            LOGGER.debug( f"Finished Monitoring ... END = {ctime()}" )
            break

        #cv2.imshow('VIDEO', frame)

        # Between Frames Secs
        #previous_dt = current_dt
        #current_dt = datetime.now()

        #current_dt_secs = current_dt.timestamp()
        #previous_dt_secs = previous_dt.timestamp()
        #elapsed_secs = current_dt_secs - previous_dt_secs

        #cv2.imwrite( f"{new_path}/frame_%d_%f.jpg" % (counter, elapsed_secs), frame)

        #try:
        LOGGER.debug( f"Ready to Capture New Frame ... {ctime()}" )
        ret, frame = vcap.read()

        if not ret:
            #raise Exception("Cannot Receive Frame (Stream End ?)")
            LOGGER.error(f"*** Cannot Receive Frame (Stream End ?) ... {'rtsp://' + username + ':' + password + '@' + ip} ***")
            break

        str_today = datetime.today().strftime( "%Y-%m-%d_%H-%M-%S" )
        #LOGGER.debug( f"Everything Happens Today ... {str_today}" )

        #cv2.imwrite( f"{new_path}/frame_%d_%s.jpg" % (counter, elapsed_secs), frame)
        #cv2.imwrite( f"{new_path}/frame_%d_%s.jpg" % (counter, str_today), frame )
        cv2.imwrite( f"{new_path}/frame_%s.jpg" % (str_today), frame )

        #except Exception as e:
        #    print( e )

        #counter += 1

        # Wait for few seconds ... Next Frame-Capture
        sleep( SLEEP_BETWEEN_SNAPSHOTS )
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Read Camera Configuration Data
def read_config():
    config = ConfigParser()
    config.sections()

    print( f"Camera-Configuration --> {config}" )

    camera_ip = config['CAMERA-A5-BACK']['camera-ip']
    username = config['CAMERA-A5-BACK']['username']
    password = config['CAMERA-A5-BACK']['password']

    global MONITORING_DURATION_MINS
    MONITORING_DURATION_MINS = int( config['CAMERA-A5-BACK']['monitoring-duration-mins'] )

    global OUTPUT_DIR
    OUTPUT_DIR = config['VIDEO-FRAMES-STORE']['output-dir']
    
    return [camera_ip, username, password]


# ***************************
#      MAIN Function
# ***************************
def main_grab():
    #camera_all = read_config()

    #global MONITORING_DURATION_MINS
    #MONITORING_DURATION_MINS = 5

    global OUTPUT_DIR
    OUTPUT_DIR = "/dt2/"

    camera_all = ["10.124.144.118", "admin", "!ntrAcom"]
    try:
        LOGGER.debug("Ready to start Frame-Grabbing from Live Camera Link")

        open_rtsp_stream(camera_all[0], camera_all[1], camera_all[2])
    except Exception as ex:
        LOGGER.error( ex )

    # Upload frames ito Google Drive
    #main_google_drive_client()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
