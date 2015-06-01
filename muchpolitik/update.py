import urllib
from urllib import request
import os
import json
import datetime
from lxml import html
import subprocess

# Since I launch that script through cron, 
# I specify where I want the images to be saved
output_dir = "."

# Where to look for images
url = "https://twitter.com/MuchPolitik/media"

def get_tweets():
	response = urllib.request.urlopen(url)
	data = response.read()
	tree = html.fromstring(data)
	tweets = tree.find_class("tweet")
	return tweets

def get_image_tweet(tweet):
	image_sections = tweet.find_class("cards-base cards-multimedia")
	if len(image_sections) == 0:
		return -1
	section = image_sections[0]
	image_url = "https:" + section.get('data-card-url')
	return image_url

def download_image(url, name):
	image_response = urllib.request.urlopen(url)
	image_data = str(image_response.read())

	image_link = image_data.split('"og:image" content="')[-1].split('">')[0]
	extension = image_link.split('.')[-1].split(':')[0]
	image_path = os.path.join(output_dir,name + "." + extension)
	if os.path.isfile(image_path):
		i = 2
		while os.path.isfile(image_path):
			image_path = output_dir + name + " - " + str(i) + "." + extension
			i += 1
	urllib.request.urlretrieve(image_link, image_path)


# We load the last saved image URL if any
saved = {}
if os.path.isfile(os.path.join(output_dir, 'muchpolitik.json')):
	saved = json.load(open(os.path.join(output_dir, '/muchpolitik.json'), 'r'))

last_image_link = ""
if "last_image_link" in saved.keys():
	last_image_link = saved["last_image_link"]

# We fetch the tweets
tweets = get_tweets()
saved["last_image_link"] = get_image_tweet(tweets[0])

new_images = 0

# And check in each of them if a new image is here
for tweet in tweets:
	latest_image = get_image_tweet(tweet)

	# If there is a new image, we download it
	if latest_image != -1 and latest_image != last_image_link:
		date = tweet.find_class("_timestamp js-short-timestamp")[0]
		date = datetime.date.fromtimestamp(int(date.get('data-time')))

		download_image(latest_image, str(date))
		new_images += 1
	else:
		break

# We save the URL of the most recent image for next time
json.dump(saved, open(output_dir + "muchpolitik.json","w"), indent=2)

# Since that script runs daily, I put a notification warning for new images
# You can comment the next lines if you don't like that
if new_images < 2:
	subprocess.Popen(['notify-send', "Updated Much Politik blog", str(new_images) + " new image downloaded."])
else:
	subprocess.Popen(['notify-send', "Updated Much Politik blog", str(new_images) + " new images downloaded."])
