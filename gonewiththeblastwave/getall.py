import urllib
from urllib import request
from lxml import html
import re

# This webcomic is over, so all we need to do is to gather everything

# Base url for the pages
url_base = "http://www.blastwave-comic.com/index.php?p=comic&nro="
# Base url for the images
image_url_base = "http://www.blastwave-comic.com/"

# We start at image 0
image_counter = 0

while True:
	# We go to the next image
	image_counter += 1

	# Fetch the appropriate page
	url = url_base + str(image_counter)
	print("Fetching: " + url)
	response = request.urlopen(url)
	data = response.read()
	tree = html.fromstring(data)

	# Find the image division in that page
	title = tree.find_class("comic_title")[0].text_content()

	# If no image was found, we reached the end of the comic
	if len(title) == 0:
		break

	# Otherwise, we find the image name
	img_name = str(image_counter) + " - " + title
	img_src = re.findall(r'img src=".*?"', str(data))[0].split('"')[1]
	img_url = image_url_base + img_src
	
	# And save it
	urllib.request.urlretrieve(img_url, img_name)
	

