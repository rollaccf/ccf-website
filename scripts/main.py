from google.appengine.ext import webapp
from google.appengine.ext.db import GqlQuery
from scripts import BaseHandler, Http404
from scripts.database_models.homepageslide import HomepageSlide
from scripts.gaesettings import gaesettings

class HomePageHandler(BaseHandler):
  def get(self):
    slides = GqlQuery("SELECT * FROM HomepageSlide WHERE Enabled = True ORDER BY DisplayOrder ASC").fetch(gaesettings.MaxHomepageSlides);
    self.render_template("index.html",
    {
      'slides':slides,
      'HomepageSlideRotationDelay':gaesettings.HomepageSlideRotationDelay,
    })


class SlideHandler(BaseHandler):
    def get(self):
      dbSlide = GqlQuery("SELECT * FROM HomepageSlide WHERE CompleteURL = :1", self.request.path).get()
      if dbSlide and dbSlide.Enabled == True:
        self.render_template("slide.html",
        { 'title':dbSlide.Title,
          'slide':dbSlide,
        },use_cache=False)
      else:
        raise Http404("Page Does Not Exist")

application = webapp.WSGIApplication([
  ('/', HomePageHandler),
  ('.*', SlideHandler),
  ], debug=BaseHandler.debug)

