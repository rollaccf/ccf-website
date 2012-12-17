import datetime
from google.appengine.ext import db
from google.appengine.ext import webapp
from scripts.database_models.homepageslide import HomepageSlide
from scripts import BaseHandler

class Image(BaseHandler):
  def get(self, encoded_key):
    try:
      slide = db.get(encoded_key)
      if slide.Image:
        two_days_in_seconds = 172800
        expires_date = datetime.datetime.now() + datetime.timedelta(days=2)
        HTTP_HEADER_FORMAT = "%a, %d %b %Y %H:%M:00 GMT"

        self.response.headers['Expires'] = expires_date.strftime(HTTP_HEADER_FORMAT)
        self.response.headers['Cache-Control'] = "public, max-age=%s" % two_days_in_seconds
        self.response.headers['Content-Type'] = "image/png"
        self.response.out.write(slide.Image)
    except:
        self.abort(404, "Image Does Not Exist")


application = webapp.WSGIApplication([
  ('/image/([^/]+)', Image),
  ], debug=BaseHandler.debug)

