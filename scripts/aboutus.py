from google.appengine.ext import webapp
from scripts import BaseHandler

class AboutUs_BaseHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(AboutUs_BaseHandler, self).__init__(*args, **kwargs)
        self.template_vars['AboutUsSelected'] = "top-level-dropdown-selected"

class BeliefsHandler(AboutUs_BaseHandler):
    def get(self):
        self.render_template("aboutus/beliefs.html")

class HistoryHandler(AboutUs_BaseHandler):
    def get(self):
        self.render_template("aboutus/history.html")

class LocationHandler(AboutUs_BaseHandler):
    def get(self):
        self.render_template("aboutus/location.html")

class StaffHandler(AboutUs_BaseHandler):
    def get(self):
        self.render_template("aboutus/staff.html")


application = webapp.WSGIApplication([
  ('/aboutus/beliefs.*', BeliefsHandler),
  ('/aboutus/history.*', HistoryHandler),
  ('/aboutus/location.*', LocationHandler),
  ('/aboutus/staff.*', StaffHandler),
  ], debug=BaseHandler.debug)
