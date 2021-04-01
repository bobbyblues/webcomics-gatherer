import urllib
from urllib import request
import time
import sys

# Hanna was here :)

# Base url for all images
url_base = "http://www.darthsanddroids.net/comics/darths"


# If the user specified an image number to start from
# We use it, otherwise, we start from the first one
try:
	i = int(sys.argv[1])
except Exception as e:
	i = 1


# As long as we can fetch images, we do so
while True:
	# Current image name
	image_name = str(i) + ".jpg"

	# Because I'm not that good at python,
	# I use a stupid hack to have the format I want for the name
	# i.e., a 4 digit number
	if i < 1000:
		image_name = "0" + image_name
	if i < 100:
		image_name = "0" + image_name
	if i < 10:
		image_name = "0" + image_name

	# And we create the current url
	url = url_base + image_name


	try:
		# We try to fetch the image
		response = urllib.request.urlretrieve(url, image_name)
		print("Downloaded " + image_name)
	except Exception as e:
		# If it fails with a 404, we fetched the most recent image and stop
		if not e.code is None and e.code == 404:
			print("Comic " + str(i - 1) + " was the last available one. Stopping.")
			print("Next time you launch that program, start it from that image using: ")
			print("python getall.py " + str(i))
			break
		else:
			# Otherwise, it's likely that we spammed the server, and make a break
			print("The server is not liking all of our requests. Waiting 30 seconds before trying again.")
			time.sleep(30)

	# Let's go to the next image
	i += 1

