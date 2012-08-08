from google.appengine.ext import webapp
from scripts.main import BaseHandler

class BeliefsHandler(BaseHandler):
    def get(self):
        self.render_template("aboutus/beliefs.html",
        {
          'AboutUsSelected':"top-level-dropdown-selected",
        })

class HistoryHandler(BaseHandler):
    def get(self):
        self.render_template("aboutus/history.html",
        {
          'AboutUsSelected':"top-level-dropdown-selected",
        })

class LocationHandler(BaseHandler):
    def get(self):
        self.render_template("aboutus/location.html",
        {
          'AboutUsSelected':"top-level-dropdown-selected",
        })

class StaffHandler(BaseHandler):
    def get(self):
        self.render_template("aboutus/staff.html",
        {
          'AboutUsSelected':"top-level-dropdown-selected",
        })


application = webapp.WSGIApplication([
  ('/aboutus/beliefs.*', BeliefsHandler),
  ('/aboutus/history.*', HistoryHandler),
  ('/aboutus/location.*', LocationHandler),
  ('/aboutus/staff.*', StaffHandler),
  ], debug=BaseHandler.debug)
