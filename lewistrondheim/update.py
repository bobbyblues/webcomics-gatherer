import urllib
from urllib import request
import re
import os
import subprocess

# I specify the output directory because I launch that script through cron
output_dir = "."

# We fetch the blog page
url_root = "http://lewistrondheim.com/blog/"
response = urllib.request.urlopen(url_root)
data = response.read()
str_data = str(data)

# We find all the images in the page
image_links = re.findall("images/[0-9]+\.jpg", str_data)
image_names = re.findall("name\=..message_[0-9]+", str_data)
image_links.sort()
image_names.sort()

new_images = 0

# We download every image in the page
for i in range(len(image_links)):
	image_link = image_links[i]
	image_name = image_names[i].split('_')[-1] + ".jpg"
	print(image_link)
	print(image_name)
	if not os.path.isfile(output_dir + image_name):
		link = url_root + image_link
		try:
			urllib.request.urlretrieve(link, output_dir + image_name)
		except Exception as e:
			print("Failed retrieving " + link + "\nError: " + str(e.code))
		new_images += 1

# Since that script runs daily, I put a notification warning for new images
# You can comment the following lines if you don't like it
if new_images < 2:
	subprocess.Popen(['notify-send', "Updated Lewis Trondheim blog", str(new_images) + " new image downloaded."])
else:
	subprocess.Popen(['notify-send', "Updated Lewis Trondheim blog", str(new_images) + " new images downloaded."])
