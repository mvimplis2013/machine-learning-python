# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from configparser import ConfigParser
from datetime import datetime
from time import sleep
import cv2
import os
#from google_client_upload_frames import main_google_drive_client

MONITORING_DURATION_MINS = 10

# Read the Camera Video Output
def open_rtsp_stream(ip, username, password):
    # Make folder to store frames
    # Date_Minute
    my_datetime = datetime.today().strftime('%Y-%m-%d-%H_%M_%S')
    new_path = f'video/frames/%s' % my_datetime

    if not os.path.exists(new_path):
        os.makedirs(new_path)

    # Grab first frame
    vcap = cv2.VideoCapture("rtsp://" + username + ":" + password + "@" + ip)
    ret, frame = vcap.read()

    current_dt = datetime.now()
    previous_dt = datetime.now()
    start_time = current_dt.timestamp()

    global MONITORING_DURATION_MINS
    monitoring_minutes = (MONITORING_DURATION_MINS * 60)
    print(f"Ready to Capture Frames for Period in Minutes = {monitoring_minutes}")

    counter = 0
    while ret:
        # Start frames capturing at ...
        time_passed = datetime.now().timestamp() - start_time
        print( f"Time Passed = %f" % time_passed)

        if time_passed > monitoring_minutes:
            break

        cv2.imshow('VIDEO', frame)

        # Between Frames Secs
        previous_dt = current_dt
        current_dt = datetime.now()

        current_dt_secs = current_dt.timestamp()
        previous_dt_secs = previous_dt.timestamp()
        elapsed_secs = current_dt_secs - previous_dt_secs

        cv2.imwrite( f"{new_path}/frame_%d_%f.jpg" % (counter, elapsed_secs), frame)

        counter += 1

        ret, frame = vcap.read()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Read Camera Configuration Data
def read_config():
    config = ConfigParser()
    config.read("camera_config")
    config.sections()

    camera_ip = config['CAMERA-A5-BACK']['camera-ip']
    username = config['CAMERA-A5-BACK']['username']
    password = config['CAMERA-A5-BACK']['password']

    global MONITORING_DURATION_MINS
    MONITORING_DURATION_MINS = int( config['CAMERA-A5-BACK']['monitoring-duration-mins'] )

    return [camera_ip, username, password]


# ***************************
#      MAIN Function
# ***************************
def main_grab():
    camera_all = read_config()
    open_rtsp_stream(camera_all[0], camera_all[1], camera_all[2])

    # Upload frames ito Google Drive
    #main_google_drive_client()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
