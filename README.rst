Webcomic gatherer
=================

This is a collection of python or shell scripts to backup webcomics I like to read.

Requires
--------
 * Python 3
 * notify-osd for the notifications (optional)

Usage
-----

Simply go to the directory of the webcomic you want and run the script:

.. code-block:: sh
	python getall.py

I tried to name my scripts such that:
 * getall scripts will download the integrality of a comic everytime you run them
 * update scripts will download the integrality of a comic the first time, and only what's missing the next times; allowing you to call those scripts regularly via cron for example


Why
---

As I am afraid one day the websites will close and I won't be able to access them anymore, I like to regularly save what I can.
I thought it might be useful for others, so I decided to share the scripts I have created over time.

If you run one of the websites targeted by those scripts and are not happy about it, please contact me and I'll remove that script from the collection.

