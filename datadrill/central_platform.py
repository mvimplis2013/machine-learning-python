import shutil

KB = 1024
MB = 1024 * KB
GB = 1024 * MB

def get_disk_usage():
	return shutil.disk_usage('/').free / GB

def platform_22():
	print(f"Ready to start system monitoring ... Free Disk Space = {get_disk_usage()}")