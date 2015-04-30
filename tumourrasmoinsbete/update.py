from lxml import html
import os
import re
import subprocess
import shutil
import time
import urllib
from urllib import request
import zipfile
import zlib

url_root = "http://tumourrasmoinsbete.blogspot.com/"
output_root = "."

months = {"janvier":"01", "février":"02", "mars":"03", "avril":"04", "mai":"05", "juin":"06", "juillet":"07","août":"08", "septembre":"09", "octobre":"10", "novembre":"11", "décembre":"12"}

curr_url = url_root
debug = False
while True:
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
	title_str = ""
	title_div = tree.find_class("post-title entry-title")

	if len(title_div) > 0:

		title_str = " - " + title_div[0].text_content()
		title_str = re.sub("\\r", "", title_str)
		title_str = re.sub("\\n", "", title_str)
		title_str = re.sub("\\t", "", title_str)
		title_str = re.sub("/", " sur ", title_str)


	# We create the output directory
	output_dir = os.path.join(output_root, date_year)
	output_dir = os.path.join(output_dir, date_month)
	output_dir = os.path.join(output_dir, date_day + title_str)

	print(output_dir)

	if os.path.isdir(output_dir):
		print("Note " + output_dir + " was already saved. Stopping.")
		break;

	try:
		os.makedirs(output_dir)
	except Exception as e:
		print("Error creating directory for " + curr_url)
		break

	# We get the note itself
	body = tree.find_class("post-body")[0]

	# We get the texte
	text = body.text_content()
	text = re.sub("\\r","", text)
	text = re.sub("\\n","\n", text)
	text = re.sub("\\t","", text)
	text = re.sub("\n+", "\n", text)
	text = re.sub("^\n", "", text)

	text_legend = False


	# We get the images
	image_files = []
	images = body.cssselect('img')
	image_id = 1
	restart = False
	for image in images:
		image_url = image.attrib['src']
		if 'title' in image.attrib:
			if not text_legend:
				text += "\nImages: "
				text_legend = True
			text += "\nImage " + str(image_id) + " : " + image.attrib['title']
		try:
			urllib.request.urlretrieve(image_url, os.path.join(output_dir, "image_" + str(image_id)))
			image_files.append("image_" + str(image_id))
		except Exception as e:
			if (e.code == 503):
				time.sleep(4.0)
				restart = True
				break
			print("\tError: " + str(e.code) + " then " + str(ee.code) + " on: " + image_url)
			break
		image_id += 1

	if restart:
		continue


	if len(image_files) > 1 and len(title_str) > 0:
		# We create the cbz file
		zf = zipfile.ZipFile(os.path.join(output_dir, "images.zip"), mode="w")
		for image_file in image_files:
			zf.write(os.path.join(output_dir, image_file), compress_type=zipfile.ZIP_DEFLATED)
		zf.close()
		os.rename(os.path.join(output_dir, "images.zip"), os.path.join(output_dir,title_str[3:] + ".cbz"))
		for image_file in image_files:
			os.remove(os.path.join(output_dir, image_file))



	with open(os.path.join(output_dir, "texte.txt"), 'w') as source:
		source.write(text)

	# We find the next article
	older_div = tree.find_class("blog-pager-older-link")
	if len(older_div) > 0:
		curr_url = older_div[0].attrib['href']
	else:
		break





	# curr_page += 1





