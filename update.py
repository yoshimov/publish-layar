#!/usr/bin/env python
#
# Copyright 2009 yoshimov

import wsgiref.handlers
from django.utils import simplejson

from google.appengine.ext import webapp
from google.appengine.ext import db
from mapdata import *

class UpdateHandler(webapp.RequestHandler):

  def get(self):
    map = Mapdata()
    map.mapname = "yoshimovucsb"
    map.title = "Harold Frank Hall"
    map.content = "sample"
    map.lat = 34.413853
    map.lon = -119.841209
    map.put()
    self.response.out.write("write done")
