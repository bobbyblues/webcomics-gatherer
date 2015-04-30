import os
import shutil
import urllib
from urllib import request
import zipfile
import zlib
import datetime


# Get comic fetches the garfield comic from a particular date
def get_comic(year, month, day, output_dir="."):
	str_month = str(month)
	if (month < 10):
		str_month = "0" + str_month
	str_day = str(day)
	if (day < 10):
		str_day = "0" + str_day
	if not os.path.isdir(output_dir):
		os.makedirs(output_dir)
	filename = str(year) + "-" + str_month + "-" + str_day + ".jpg"
	try:
		image_link = "http://garfield.com/uploads/strips/" + filename
		urllib.request.urlretrieve(image_link, os.path.join(output_dir, filename))
	except Exception as e:
		print("Fetching " + filename + ":" + str(e.code))
		return		


# We get today's date as a starting point for the download
date = datetime.datetime.now()
year = date.year
# Since we want to download whole months to create cbz archives, 
# we start from the previous month
month = date.month - 1
if (month < 0):
	year = year - 1
	month = 12


# We download all images until we encounter a file already downloaded
while True:
	# We create the proper URL for the current comic
	str_month = str(month)
	# Stupid but easy way to format the string the way I want
	if (month < 10):
		str_month = "0" + str_month
	# We create the path for the current month
	curr_output_dir = os.path.join(str(year), str_month)
	curr_output_path = os.path.join(".", curr_output_dir)
	curr_output_file = curr_output_dir + ".cbz"

	# If we meet an already downloaded comic, we stop
	if (os.path.isfile(curr_output_file)):
		break

	# Otherwise, we download the comic of each day in the month
	# (plus some extras days, just to be sure :))
	for day in range(1, 32):
		get_comic(year, month, day, curr_output_path)
	# We can store the result in a zip file
	zf = zipfile.ZipFile(curr_output_dir + ".zip", mode="w")
	for filename in os.listdir(curr_output_path):
		zf.write(os.path.join(curr_output_path, filename), compress_type=zipfile.ZIP_DEFLATED)
	zf.close()
	# And rename that zip file into cbz
	os.rename(curr_output_dir+".zip", curr_output_dir+".cbz")

	# Finally we remove the images
	shutil.rmtree(curr_output_dir)

	# And go to the previous month
	month -= 1
	if month :
		month = 12
		year -= 1

	# If we got before the creation of the comic, we stop
	if year == 1978 and month < 6:
		print("That's all folks. Everything has been gathered!")