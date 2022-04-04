from os import listdir
import time

SLEEP_SECS = 10

def count_frames(folder):
	files_dirs = listdir(folder)
	print(f"Number of Frames .... {files_dirs}")

def run_watchdog():
	data_dir = "/dt2/video/frames/"

	while True:
		count_frames(data_dir)
		time.sleep(3)

