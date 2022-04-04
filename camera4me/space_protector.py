from os import listdir

def count_frames(folder):
	files_dirs = listdir(folder)


	print(f"Number of Frames .... {len(files_dirs)}")

def run_watchdog():
	data_dir = "/dt2"

	while True:
		count_frames(data_dir)