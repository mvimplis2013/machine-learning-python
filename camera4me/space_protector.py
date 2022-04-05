from os import listdir, chdir
import time

SLEEP_SECS = 10

def count_frames(folder):
	try:
		files_dirs = listdir(folder)
	except OSError as x:
		print(f"Cannot change into FRAMES folder ... {x}")
		exit(1)

	print(f"Folders inside Frames = {files_dirs}")

	# try:
	# 	chdir(files_dirs)
	# except OSError as x:
	# 	print(f"Cannot change into DATE folder ... {x}")
	# 	exit(1)
	
	# files_dirs = listdir('.')
	# print(f"Number of Frames .... {len(files_dirs)}")

def run_watchdog():
	data_dir = "/dt2/video/frames/"

	while True:
		count_frames(data_dir)
		#time.sleep(3)

