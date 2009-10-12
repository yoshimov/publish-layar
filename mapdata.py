from google.appengine.ext import db

class Mapdata(db.Model):
  mapname = db.StringProperty()
  author = db.UserProperty(auto_current_user=True)
  title = db.StringProperty()
  content = db.TextProperty()
  lat = db.FloatProperty()
  lon = db.FloatProperty()
