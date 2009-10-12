#!/usr/bin/env python
#
# Copyright 2009 Yoshimov



import wsgiref.handlers
from search import *
from update import *

from google.appengine.ext import webapp

def main():
  application = webapp.WSGIApplication([
	('/search', SearchHandler),
	('/update', UpdateHandler)], debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
