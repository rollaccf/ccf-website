from google.appengine.ext import webapp
from scripts.main import BaseHandler

class BeliefsHandler(BaseHandler):
    def get(self):
        self.render_template("aboutus/beliefs.html",
        { 'title':"CCF Beliefs",
          'AboutUsSelected':"top-level-dropdown-selected",
        })

class HistoryHandler(BaseHandler):
    def get(self):
        self.render_template("aboutus/history.html",
        { 'title':"CCF History",
          'AboutUsSelected':"top-level-dropdown-selected",
        })

class LocationHandler(BaseHandler):
    def get(self):
        self.render_template("aboutus/location.html",
        { 'title':"CCF Location",
          'AboutUsSelected':"top-level-dropdown-selected",
        })

class StaffHandler(BaseHandler):
    def get(self):
        self.render_template("aboutus/staff.html",
        { 'title':"CCF Staff",
          'AboutUsSelected':"top-level-dropdown-selected",
        })


application = webapp.WSGIApplication([
  ('/aboutus/beliefs.*', BeliefsHandler),
  ('/aboutus/history.*', HistoryHandler),
  ('/aboutus/location.*', LocationHandler),
  ('/aboutus/staff.*', StaffHandler),
  ], debug=True)
