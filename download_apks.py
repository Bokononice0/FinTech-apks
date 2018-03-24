from sys import argv
import os
import csv
from pathlib import Path

def download_apk(apk_id):
	# if apk already exists, then ignore
	filename = "{0}.apk".format(apk_id)
	path = Path(filename)
	if path.is_file():
		print("{0} already exists!".format(apk_id))
		return
	# else download
	os.system("gplaycli --progress -d {0}".format(apk_id))

def get_apk_ids(path):
	# Read CSV
	# Look for all APK IDs present
	# Return a list of APK IDs
	
	def get_apk_id(s):
		if '?id=' not in s:
			return None
		return s.split('?id=')[1].split()[0]

	apk_ids = []
	with open(path) as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			if len(row) < 4:
				continue
			apk_id = get_apk_id(row[3])
			if apk_id is not None:
				apk_ids.append(apk_id)
	return apk_ids

def display(apk_ids):
	print("Found the following APKs:")
	for idx, apk_id in enumerate(apk_ids):
		print("{0}. {1}".format(idx + 1, apk_id))

def main():
	if len(argv) < 2:
		print("Usage: python download_apks.py <PATH_TO_CSV>")
		exit(0)
	
	path = argv[1]
	apk_ids = get_apk_ids(path)
	display(apk_ids)

	for counter in range(len(apk_ids)):
		try:
			print("[{0}/{1}] Downloading: {2}".format(counter + 1, len(apk_ids), apk_ids[counter]))
			download_apk(apk_ids[counter])
		except:
			print("FAILED! {0} could not be downloaded :(".format(apk_ids[counter]))
	
if __name__ == '__main__':
	main()
