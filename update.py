#!/usr/bin/env python
#
# Copyright 2009 yoshimov

import wsgiref.handlers
from django.utils import simplejson
import feedparser

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from mapdata import *

class UpdateHandler(webapp.RequestHandler):

  def get(self):
	# authentication
	if not users.is_current_user_admin():
	  self.redirect(users.create_login_url(self.request.url))
	  return
	self.response.out.write("""
<html>
<body>
Please specify georss url:
<form method="post">
<p>
Layer name:
<input type="text" name="layername" />
</p>
<p>
Georss url:
<input type="text" name="url" />
</p>
<input type="submit" name="post" />
</form>
</body>
</html>
""")

  def post(self):
	# authentication
	if not users.is_current_user_admin():
	  self.redirect(users.create_login_url(self.request.url))
	  return
	layername = self.request.get("layername")
	url = self.request.get("url")

	# clear existing data
	keys = db.GqlQuery("SELECT __key__ FROM Mapdata WHERE mapname=:1", layername).fetch(200)
	db.delete(keys)
	
	feed = feedparser.parse(url)
	self.response.out.write("<p>feed title: %s</p>" % feed.channel.title)

	for item in feed.entries:
	  self.response.out.write("<p><li>title: %s</li>" % item.title)
	  self.response.out.write("<li>descrption: %s</li>" % item.description)

	  points = item.point.split(" ")
	  lat = float(points[0])
	  lon = float(points[1])
	  self.response.out.write("<li>geopoint: %f,%f</li></p>" % (lat, lon))
	  map = Mapdata()
	  map.mapname = layername
	  map.title = item.title
	  map.content = item.description
	  map.lat = lat
	  map.lon = lon
	  map.put()
	self.response.out.write("update POIs done")
