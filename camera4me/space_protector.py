from os import listdir, chdir, remove
from os.path import isfile, isdir, getmtime
import time
from datetime import datetime

SLEEP_SECS = 10

DAYS_OLD  = 1    # One Day
HOURS_OLD = 2    # Two Hours

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

def inside_date_folder(folder):
	chdir(folder)
	files = listdir('.')
	#print(f"Number of Frames inside Folder .... {len(files)} / {folder}")

	now = datetime.now()
	
	for f in files:
		if isfile(f):
			then = datetime.fromtimestamp( getmtime(f) )
			tdelta = now - then

			days    = tdelta.days
			seconds = tdelta.seconds
			minutes = seconds / 60.0
			hours   = minutes / 60.0
			#days    = hours / 24

			if older_than_days(days):
				print(f"Ready to Delete Frame More Than Day(s) Old .... {f} / {days}-(days)")
				remove(f)
			elif older_than_hours(hours):
				print(f"Ready to Delete Frame More Than Hours(s) Old .... {f} / {hours}-(hrs)")
				remove(f)
			
def count_frames(folder):
	try:
		chdir(folder)
		files_dirs = listdir(".")
	except OSError as x:
		print(f"Cannot change into FRAMES folder ... {x}")
		exit(1)

	#print(f"Folders inside Frames = {files_dirs}")
	
	for f in files_dirs:
		if isdir(f):
			inside_date_folder(f)

def run_watchdog():
	data_dir = "/dt2/video/frames/"

	while True:
		count_frames(data_dir)
		#time.sleep(3)

