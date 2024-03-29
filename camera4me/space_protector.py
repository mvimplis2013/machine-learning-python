from os import listdir, chdir, remove, rmdir
from os.path import isfile, isdir, getmtime
import time
from datetime import datetime

import subprocess

import http.server
from prometheus_client import start_http_server

import logging
LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s')
logging.basicConfig( level=logging.DEBUG, format=LOG_FORMAT )

LOGGER = logging.getLogger( __name__ )

class ServerHandler(http.server.BaseHTTPRequestHandler):
  def do_GET(self):
    self.send_response(200)
    self.end_headers()
    self.wfile.write(b"Hello World!") 

SLEEP_SECS = 3

DAYS_OLD    = 1    # One Day
HOURS_OLD   = 2    # Two Hours
MINUTES_OLD = 2    # Two(2) Minutes

DELETE_EMPTY_FOLDERS_AFTER_SECS = 10*60  # Minutes

def older_than_days(days):
	if days >= DAYS_OLD:
		return True
	else:
		return False

def older_than_hours(hours):
	if hours >= HOURS_OLD:
		return True
	else:
		return False

def older_than_minutes(minutes):
	if minutes >= MINUTES_OLD:
		return True
	else:
		return False

def inside_date_folder(folder):
	files = listdir(folder)
	
	# Current Time
	now = datetime.now()

	then = datetime.fromtimestamp( getmtime(folder) )
	tdelta = now - then

	# Check existing folders 
	if isdir(folder) & (tdelta.total_seconds() > DELETE_EMPTY_FOLDERS_AFTER_SECS) & (len(files) == 0):
		# Empty + Old Directory
		LOGGER.debug(f"Ready to Remove an Empty Folder ... {folder}")
		rmdir(folder)

		return

	if (now.minute % 10 == 0) & (now.second < 10):
		# Every 10 minutes
		LOGGER.debug(f"Number of Frames inside Folder .... {now.strftime('%Y-%m-%d %H:%M:%S')} : {folder} --> {len(files)}")

	for f in files:
		#print(f"Current Frame .... {f} / isFile = {isfile(f)}")

		##if f.startswith( "frame_" ) & f.endswith( ".jpg" ):
		if f.find("frame_") >= 0 and f.endswith(".jpg"):
			# A video-snapshot
			f = folder + '/' + f
			#print(f"Current Frame Path Name .... {f}")

			then = datetime.fromtimestamp( getmtime(f) )
			tdelta = now - then

			#days    = tdelta.days

			seconds = tdelta.total_seconds()

			minutes = seconds / 60.0
			hours   = minutes / 60.0
			days    = hours / 24

			#if now.minute % 10 == 0:
			#	print(f"Frame Creation Time .... {f} --> {hours}-(hrs) , {minutes}-(mins)")

			if older_than_days(days):
				LOGGER.debug(f"Ready to Delete Frame More than Day(s) Old .... {f} / {days}-(days)")
				remove(f)
			elif older_than_hours(hours):
				LOGGER.debug(f"Ready to Delete Frame More than Hours(s) Old .... {f} / {hours}-(hrs)")
				remove(f)
			elif older_than_minutes(minutes):
				LOGGER.debug(f"Ready to Delete Frame More than TWO Minute(s) Old ... {f} / {minutes}-(mins)")
				remove(f)
			
def count_frames(folder):
	try:
		chdir(folder)
		files_dirs = listdir(".")
	except OSError as x:
		LOGGER.debug(f"Cannot change into FRAMES folder ... {x}")
		exit(1)

	LOGGER.debug(f"Folders inside Frames = {files_dirs}")
	
	for f in files_dirs:
		if isdir(f):
			inside_date_folder(f)

def run_watchdog():
	#start_http_server(9090)
	#server = http.server.HTTPServer(('', 9091), ServerHandler)
	#print('Prometheus Metrics Available on Port 9090 / metrics')
	#print('HTTP Server available on port 9091')
	#server.serve_forever()
	
	LOGGER.debug(f"Ready to start hard-disk watchdog")

	#subprocess.call([ "polite-messenger", "-n", "vibm-mq" ])

	#subprocess.call( [ "influxdb-caller" ])

	data_dir = "/dt2/video/frames/"

	while True:
		count_frames(data_dir)

		# No Sleep = 1500 frames / Minute
		time.sleep( SLEEP_SECS )

