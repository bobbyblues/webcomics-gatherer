Webcomic gatherer
=================

This is a collection of python or shell scripts to backup webcomics I like to read.

Requires
--------

For baldouine:
 * sh and wget

For Les autres gens:
 * Python 2 with mechanize

For the rest:
 * Python 3
 * notify-osd for the notifications (optional)

General usage
-----

Simply go to the directory of the webcomic you want and run the script:

.. code-block:: sh
	python getall.py


I tried to name my scripts such that:
 * getall scripts will download the integrality of a comic everytime you run them
 * update scripts will download the integrality of a comic the first time, and only what's missing the next times; allowing you to call those scripts regularly via cron for example


Les autres gens
----
Because Les autres gens requires an account, you need to provide your credentials.
To do so, change the "???" in the file credential.json by your username and password.
You can then download the two complete seasons by running:

.. code-block:: sh
	python2 getall.py

Or download a specific episode by running:

.. code-block:: sh
	python2 getEpisode.py url title


For example, one could download the first episode as:

.. code-block:: sh
	python getEpisode.py "http://www.lesautresgens.com/Episode-1-Le-1-le-2-le-3" "Episode 1"


Note that this does not allow an illegal download of this webcomic, and if you don't have valid credential, you will only download the preview of each episode.


Why
---

As I am afraid one day the websites will close and I won't be able to access them anymore, I like to regularly save what I can.
I thought it might be useful for others, so I decided to share the scripts I have created over time.

If you run one of the websites targeted by those scripts and are not happy about it, please contact me and I'll remove that script from the collection.

