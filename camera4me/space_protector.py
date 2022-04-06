from os import listdir, chdir, remove, rmdir
from os.path import isfile, isdir, getmtime
import time
from datetime import datetime

SLEEP_SECS = 10

DAYS_OLD    = 1    # One Day
HOURS_OLD   = 2    # Two Hours
MINUTES_OLD = 10   # Ten Minutes

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
		print(f"Ready to Remove an Empty Folder ... {folder}")
		rmdir(folder)

		return

	if (now.minute % 10 == 0) & (now.second < 10):
		# Every 10 minutes
		print(f"Number of Frames inside Folder .... {now.strftime('%Y-%m-%d %H:%M:%S')} : {folder} --> {len(files)}")

	for f in files:
		print(f"Current Frame .... {f} / isFile = {isfile(f)}")

		if f.startswith( "frame_" ) & f.endswith( ".jpg" ):
			# A video-snapshot
			f = folder + '/' + f

			print(f"Current Frame After File Test .... {f}")

			then = datetime.fromtimestamp( getmtime(f) )
			tdelta = now - then

			#days    = tdelta.days

			seconds = tdelta.total_seconds()

			minutes = seconds / 60.0
			hours   = minutes / 60.0
			days    = hours / 24

			print(f"File Modification Time .... {f} --> {days}-(days) , {hours}-(hrs) , {minutes}-(mins)")

			if now.minute % 10 == 0:
				print(f"File Modification Time .... {f} --> {hours}-(hrs) , {minutes}-(mins)")

			if older_than_days(days):
				print(f"Ready to Delete Frame More than Day(s) Old .... {f} / {days}-(days)")
				remove(f)
			elif older_than_hours(hours):
				print(f"Ready to Delete Frame More than Hours(s) Old .... {f} / {hours}-(hrs)")
				remove(f)
			elif older_than_minutes(minutes):
				print(f"Ready to Delete Frame More than Minute(s) Old ... {f} / {minutes}-(mins)")
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

