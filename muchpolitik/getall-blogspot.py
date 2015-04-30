# -*- coding: utf-8 -*- 
from lxml import html
import re
import time
import urllib
from urllib import request

# The goal of this script is to download everything from the now abandonned
# Muchpolitik blogspot

url_root = "http://muchpolitik.blogspot.com/"
output_root = "."

# Handful dictionary
months = {"janvier":"01", "février":"02", "mars":"03", "avril":"04", "mai":"05", "juin":"06", "juillet":"07","août":"08", "septembre":"09", "octobre":"10", "novembre":"11", "décembre":"12"}

curr_url = url_root
while True:
	# We fetch the current page
	response = urllib.request.urlopen(curr_url)
	data = response.read()
	data_str = str(data)
	full_tree = html.fromstring(data)

	# We get all the articles from the current page
	articles = full_tree.find_class("date-outer")
	for tree in articles:

		# We try to find the date
		date = tree.find_class("date-header")
		if len(date) == 0:
			# We reached the last page
			break

		# We compute the image string
		date_split = date[0].text_content().split(' ')
		date_day = date_split[1]
		if int(date_day) < 10:
			date_day = "0" + date_day
		date_month_str = date_split[2]
		if not date_month_str in months.keys():
			if (date_month_str[0] == 'f'):
				date_month_str = "février"
			elif (date_month_str[0] == 'd'):
				date_month_str = "décembre"
			else:
				print ("Error in months for " + curr_url)
				print(date_month_str)
				break
		date_month = months[date_month_str]
		date_year = date_split[3]
		date_str = date_year + "-" + date_month + "-" + date_day


		# And start downloading the articles
		inner_articles = tree.find_class("post-outer")
		for inner_tree in inner_articles:

			# We get the title of the note
			title_str = ""
			title_div = inner_tree.find_class("post-title entry-title")

			if len(title_div) > 0:

				title_str = " - " + title_div[0].text_content()
				title_str = re.sub("\\r", "", title_str)
				title_str = re.sub("\\n", "", title_str)
				title_str = re.sub("\\t", "", title_str)
				title_str = re.sub("/", " sur ", title_str)


			# We get the images
			body = inner_tree.find_class("post-body")[0]
			images = body.cssselect('img')
			image_id = 1
			restart = False
			for image in images:
				image_url = image.attrib['src']
				try:
					urllib.request.urlretrieve(image_url, date_str + title_str + ".jpg")
					print("Getting " + image_url)
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

	# We find the next article
	older_div = full_tree.find_class("blog-pager-older-link")
	if len(older_div) > 0:
		curr_url = older_div[0].attrib['href']
	else:
		break

