from os.path import join
from google.appengine.ext import webapp
from google.appengine.ext.db import GqlQuery, to_dict
from scripts.main import BaseHandler
from scripts.database_models import HomepageSlide

class SlideHandler(BaseHandler):
    def get(self):
      dbSlide = GqlQuery("SELECT * FROM HomepageSlide WHERE CompleteURL = :1", self.request.path).get()
      # TODO: add error checking
      if dbSlide == None:
        pass
      else:
        slide = to_dict(dbSlide)
        slide['key'] = dbSlide.key()
      self.render_template("slide.html",
        { 'title':slide["Title"],
          'slide':slide,
        })


application = webapp.WSGIApplication([
  ('/slide.*', SlideHandler),
  ], debug=True)
