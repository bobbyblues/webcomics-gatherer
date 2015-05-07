# -*- coding: utf-8 -*- 
import sys
import re
import os
import zipfile
import zlib
import urllib
import shutil
import mechanize
import json
import argparse

def getEpisode(lines, title, output_dir):
	print("Downloading " + title)
	images = []

	# If a line contains an image, we store it in the images array
	for line in lines:
		if re.search('/bd/', line):
			temp = line.split("'")
			if (len(temp)>1):
				images.append(temp[1])


	# We create a directory to store that episode
	directory = output_dir
	if not os.path.isdir(directory):
		os.mkdir(directory)

	# We get the image format for this episode
	ext = images[0].split('.')[-1];

	# We download each image one by one
	i = 1;
	for image in images:
		urllib.urlretrieve("http://www.lesautresgens.com"+image, directory+"/"+str(i)+"."+ext)
		i = i + 1;

	# We compress the directory as a .zip
	zf = zipfile.ZipFile(directory + ".zip", mode="w")
	for filename in os.listdir(directory):
		zf.write(directory+"/"+filename, compress_type=zipfile.ZIP_DEFLATED)
	zf.close()

	# We rename the .zip as a .cbz
	os.rename(directory+".zip", title+".cbz")

	# We delete the directory with the images
	shutil.rmtree(directory)


# ============================================================================ #
# Main
# ============================================================================ #
if __name__ == "__main__":
	

	# Parsing arguments
	# =======
	parser = argparse.ArgumentParser()
	parser.add_argument('url', help="URL de l'épisode à télécharger")
	parser.add_argument('titre', help="Titre de l'épisode")
	opts = parser.parse_args()
	url = opts.url
	title = opts.titre


	# Login
	# =======
	br = mechanize.Browser()
	login_url = "http://www.lesautresgens.com/spip.php?page=votrecompte"
	br.open(login_url) # We open the login page
	br.select_form(nr = 0) # We select the login form
	credentials = json.load(open("utilisateur.json",'r'))
	br.form['var_login'] = credentials["utilisateur"]
	br.form['password'] = credentials["mot_de_passe"]
	br.submit()

	# Downloading the webpage
	# =======
	response = br.open(url)
	lines = str(response.read()).split("\n")

	# Getting the title
	# =======
	for line in lines:
		if re.search('<title>', line):
			title = line.split('>')[1].split('<')[0]

	# Downloading the episode
	# =======
	getEpisode(lines, title, "tmp")





	