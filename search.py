#!/usr/bin/env python
#
# Copyright 2009 yoshimov

import math
import re
import wsgiref.handlers
from django.utils import simplejson
from google.appengine.ext import webapp

from mapdata import *

class SearchHandler(webapp.RequestHandler):

  def get(self):
	layername = self.request.get("layerName", default_value="yoshimovucsb")
	reqlat = float(self.request.get("lat", default_value="0"))
	reqlon = float(self.request.get("lon", default_value="0"))
	radius = float(self.request.get("radius", default_value="500"))/50000
	# Search key
	searchkey = self.request.get("SEARCHBOX", default_value=None)
	maps = []

	if searchkey != None:
	  # fetch whole points
	  maps = db.GqlQuery("SELECT * FROM Mapdata WHERE mapname=:1", layername)
	elif reqlat != 0:
	  # filter by lat
	  maps = db.GqlQuery("SELECT * FROM Mapdata WHERE mapname=:1 and lat<:2 and lat>:3", layername, reqlat + radius, reqlat - radius)
	else:
	  # first 20 only (for test only)
	  maps = db.GqlQuery("SELECT * FROM Mapdata WHERE mapname=:1 limit 20", layername)

	hotspots = []
	for map in maps:
	  if searchkey != None:
		if map.title.lower().find(searchkey.lower()) < 0 and (map.content == None or map.content.lower().find(searchkey.lower()) < 0):
		  continue
	  item = {"actions": [], "attribution": None, "imageURL": None,
		"line2": None, "line3": None, "line4": None, "type": 0}
	  item["id"] = "item%d" % map.key().id()
	  if reqlat != 0:
	    item["distance"] = math.sqrt((map.lat - reqlat)**2 + ((map.lon - reqlon)*1.1)**2)
	  else:
	    item["distance"] = 0
	  if map.content != None:
		item["attribution"] = ""
		for line in map.content.splitlines():
		  if line.startswith("2:"):
			item["line2"] = line[2:]
		  elif line.startswith("3:"):
			item["line3"] = line[2:]
		  elif line.startswith("4:"):
			item["line4"] = line[2:]
		  elif line.startswith("image:"):
			item["imageURL"] = line[6:]
		  elif line.startswith("tel:"):
			action = {"uri": line, "label": "Call this spot"}
			item["actions"].append(action)
		  elif line.startswith("mailto:"):
			action = {"uri": line, "label": "Send mail"}
			item["actions"].append(action)
		  elif line.startswith("http:"):
			action = {"uri": line, "label": "More info"}
			item["actions"].append(action)
		  else:
			item["attribution"] = item["attribution"] + line + "\n"
	  if re.match("\d:", map.title):
		item["type"] = int(map.title[0])
		item["title"] = map.title[2:]
	  else:
		item["title"] = map.title
	  item["lat"] = long(map.lat * 10**6)
	  item["lon"] = long(map.lon * 10**6)
	  hotspots.append(item)
	hotspots.sort(cmp=lambda x, y: cmp(x["distance"], y["distance"]))
	if len(hotspots) > 20:
	  del hotspots[20:]

	ret = {"hotspots": hotspots, "layer": layername,
		"errorCode": 0, "errorString": "ok",
		"nextPageKey": None, "morePages": False}
	self.response.out.write(simplejson.dumps(ret))
