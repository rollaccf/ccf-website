from google.appengine.ext import db
from google.appengine.ext import webapp
from scripts.database_models import HomepageSlide

class Image(webapp.RequestHandler):
  def get(self):
    key = self.request.get("key")
    if key:
      slide = db.get(key)
      if slide.Image:
        self.response.headers['Content-Type'] = "image/png"
        self.response.out.write(slide.Image)
      else:
        self.response.out.write("No image")


application = webapp.WSGIApplication([('/image', Image)], debug=BaseHandler.debug)

