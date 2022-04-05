from os import listdir, chdir
from os.path import isfile, isdir
import time

SLEEP_SECS = 10

def inside_date_folder(folder):
	chdir(folder)
	files_dirs = listdir('.')
	print(f"Number of Frames .... {len(files_dirs)}")

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

