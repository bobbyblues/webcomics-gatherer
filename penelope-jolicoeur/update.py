from lxml import html
import os
import re
import urllib
from urllib import request



url_root = "http://www.penelope-jolicoeur.com/page/"
output_root = "." # We output in the current directory

months = {"janvier":"01", "février":"02", "mars":"03", "avril":"04", "mai":"05", "juin":"06", "juillet":"07","août":"08", "septembre":"09", "octobre":"10", "novembre":"11", "décembre":"12"}

curr_page = 1

while True:
	curr_url = url_root + str(curr_page)
	print("Downloading " + curr_url)

	response = urllib.request.urlopen(curr_url)
	data = response.read()
	data_str = str(data)
	tree = html.fromstring(data)

	# We try to find the date
	date = tree.find_class("date-header")
	if len(date) == 0:
		# We reached the last page
		break

	date_split = date[0].text_content().split(' ')
	date_day = date_split[1]
	date_month_str = date_split[2]
	if not date_month_str in months.keys():
		print ("Error in months for " + curr_url)
		break
	date_month = months[date_month_str]
	date_year = date_split[3]

	# We get the title of the note
	title_str = tree.find_class("entry-header")[0].text_content()
	title_str = re.sub("\\r", "", title_str)
	title_str = re.sub("\\n", "", title_str)
	title_str = re.sub("\\t", "", title_str)


	# We create the output directory
	output_dir = os.path.join(output_root, date_year)
	output_dir = os.path.join(output_dir, date_month)
	output_dir = os.path.join(output_dir, date_day + " - " + title_str)

	if os.path.isdir(output_dir):
		# We already downloaded that note, we stop
		break

	try:
		os.makedirs(output_dir)
	except Exception as e:
		print("Error creating directory for " + curr_url)
		break

	# We get the note itself
	body = tree.find_class("entry-body")[0]

	# We get the texte
	text = body.text_content()
	text = re.sub("\\r","", text)
	text = re.sub("\\n","\n", text)
	text = re.sub("\\t","", text)

	text_legend = False


	# We get the images
	images = body.cssselect('img')
	image_id = 1
	for image in images:
		image_url = image.attrib['src']
		if 'title' in image.attrib:
			if not text_legend:
				text += "\nImages: "
				text_legend = True
			text += "\nImage " + str(image_id) + " : " + image.attrib['title']
		try:
			urllib.request.urlretrieve(image_url, os.path.join(output_dir, "image_" + str(image_id)))
		except Exception as e:
			temp = image_url.split("photos")
			image_url = temp[0] + "photos" + re.sub('-','',temp[1])
			try:
				urllib.request.urlretrieve(image_url, os.path.join(output_dir, "image_" + str(image_id)))
			except Exception as ee:
				print("\tError: " + str(e.code) + " then " + str(ee.code) + " on: " + image_url)
				break
		image_id += 1


	with open(os.path.join(output_dir, "texte.txt"), 'w') as source:
		source.write(text)

	curr_page += 1





