from os import listdir, chdir
from os.path import isfile, isdir, getmtime
import time
from datetime import datetime

SLEEP_SECS = 10

def inside_date_folder(folder):
	chdir(folder)
	files = listdir('.')
	print(f"Number of Frames inside Folder .... {len(files)} / {folder}")

	now = datetime.now()
	
	for f in files:
		if isfile(f):
			then = datetime.fromtimestamp( getmtime(f) )
			tdelta = now - then

			#days    = tdelta.days
			seconds = tdelta.total_seconds()
			minutes = seconds / 60.0
			hours   = minutes / 60.0
			days    = hours / 24

			print(f"Total Seconds Since File Modification Time .... {f} / {seconds}secs / {minutes}mins / {hours}hrs / {days}days")
			
def count_frames(folder):
	try:
		chdir(folder)
		files_dirs = listdir(".")
	except OSError as x:
		print(f"Cannot change into FRAMES folder ... {x}")
		exit(1)

	print(f"Folders inside Frames = {files_dirs}")
	
	for f in files_dirs:
		if isdir(f):
			inside_date_folder(f)

def run_watchdog():
	data_dir = "/dt2/video/frames/"

	while True:
		count_frames(data_dir)
		#time.sleep(3)

