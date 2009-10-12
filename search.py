#!/usr/bin/env python
#
# Copyright 2009 yoshimov

import math
import wsgiref.handlers
from django.utils import simplejson
from google.appengine.ext import webapp

from mapdata import *

class SearchHandler(webapp.RequestHandler):

  def get(self):
	layername = self.request.get("layerName", default_value="yoshimovucsb")
	reqlat = float(self.request.get("lat", default_value="0"))
	reqlon = float(self.request.get("lon", default_value="0"))
	# Search key
	searchkey = self.request.get("SEARCHBOX", default_value=None)
	maps = []

	if searchkey != None:
	  # fetch whole points
	  maps = db.GqlQuery("SELECT * FROM Mapdata WHERE mapname=:1", layername)
	elif reqlat != 0:
	  # filter by lat
	  maps = db.GqlQuery("SELECT * FROM Mapdata WHERE mapname=:1 and lat<:2 and lat>:3", layername, reqlat + 0.02, reqlat - 0.02)
	else:
	  # first 20 only (for test only)
	  maps = db.GqlQuery("SELECT * FROM Mapdata WHERE mapname=:1 limit 20", layername)

	hotspots = []
	for map in maps:
	  if searchkey != None:
		if map.title.lower().find(searchkey.lower()) < 0:
		  continue
	  item = {"actions": [], "attribution": None, "imageURL": None,
		"line2": None, "line3": None, "line4": None, "type": 0}
	  item["id"] = "item%d" % map.key().id()
	  if reqlat != 0:
	    item["distance"] = math.sqrt((map.lat - reqlat)**2 + (map.lon - reqlon)**2)
	  else:
	    item["distance"] = 0
	  item["title"] = map.title
	  item["line2"] = map.content
	  item["lat"] = long(map.lat * pow(10, 6))
	  item["lon"] = long(map.lon * pow(10, 6))
	  hotspots.append(item)
	hotspots.sort(cmp=lambda x, y: cmp(x["distance"], y["distance"]))
	if len(hotspots) >= 20:
	  del hotspots[20:]

	ret = {"hotspots": hotspots, "layer": layername,
		"errorCode": 0, "errorString": "ok",
		"nextPageKey": None, "morePages": False}
	self.response.out.write(simplejson.dumps(ret))
