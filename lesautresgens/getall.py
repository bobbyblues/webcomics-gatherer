import mechanize
import re
import json
from getEpisode import getEpisode
import os
import time


br = mechanize.Browser()


# Login
# =======

login_url = "http://www.lesautresgens.com/spip.php?page=votrecompte"
br.open(login_url) # We open the login page
br.select_form(nr = 0) # We select the login form
credentials = json.load(open("utilisateur.json",'r'))
br.form['var_login'] = credentials["utilisateur"]
br.form['password'] = credentials["mot_de_passe"]
br.submit()


# Loading episode list
# =======
episodes = json.load(open('episodes.json'))
saison1 = episodes['saison1']
saison2 = episodes['saison2']



base_url = "http://www.lesautresgens.com/"

# Downloading season 1
# =======
if not os.path.isdir("saison 1"):
		os.mkdir("saison 1")
for key in saison1.keys():
	value = saison1[key]
	url = base_url + value[0]
	response = br.open(url)
	data = str(response.read()).split("\n")
	title = key + " - " + value[1]
	got_episode = False
	if os.path.isfile("saison 1/" + title + ".cbz"):
		print("Skipping: " + title)
		continue

	while not got_episode:
		try:
			getEpisode(data, title, "tmp")
			got_episode = True
		except Exception as e:
			print("Download failed, waiting 30 seconds")
			print("Error was: ")
			print(e)
			time.sleep(30)

	os.rename(title + ".cbz", "saison 1/" + title + ".cbz" )

# ==============================================================================
# Downloading season 2
# =======
if not os.path.isdir("saison 2"):
		os.mkdir("saison 2")
for key in saison2.keys():
	value = saison2[key]
	url = base_url + value[0]
	response = br.open(url)
	data = str(response.read()).split("\n")
	title = key + " - " + value[1]
	got_episode = False
	if os.path.isfile("saison 2/" + title + ".cbz"):
		print("Skipping: " + title)
		continue

	while not got_episode:
		try:
			getEpisode(data, title, "tmp")
			got_episode = True
		except Exception as e:
			print("Download failed, waiting 30 seconds")
			print("Error was: ")
			print(e)
			time.sleep(30)

	os.rename(title + ".cbz", "saison 2/" + title + ".cbz" )
