from google.appengine.ext import db
from google.appengine.ext import webapp
from scripts.database_models.homepageslide import HomepageSlide
from scripts import BaseHandler, Http404

class Image(BaseHandler):
  def get(self, encoded_key):
    try:
      slide = db.get(encoded_key)
      if slide.Image:
        self.response.headers['Content-Type'] = "image/png"
        self.response.out.write(slide.Image)
    except:
      raise Http404("Image Does Not Exist")


application = webapp.WSGIApplication([
  ('/image/([^/]+)', Image),
  ], debug=BaseHandler.debug)

