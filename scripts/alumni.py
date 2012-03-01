from google.appengine.ext import webapp
from scripts.main import BaseHandler

class MinistryHappeningsHandler(BaseHandler):
    def get(self):
        self.render_template("alumni/ministry_happenings.html",
        { 'title':"CCF Alumni",
          'headerText':"Ministry Happenings",
          'AlumniSelected':"top-level-dropdown-selected",
        })

class PastEventsHandler(BaseHandler):
    def get(self):
        self.render_template("alumni/past_events.html",
        { 'title':"CCF Alumni",
          'headerText':"Past Events",
          'AlumniSelected':"top-level-dropdown-selected",
        })

class DonateHandler(BaseHandler):
    def get(self):
        self.render_template("alumni/donate.html",
        { 'title':"CCF Alumni",
          'headerText':"Donate",
          'AlumniSelected':"top-level-dropdown-selected",
        })


application = webapp.WSGIApplication([
  ('/alumni/ministry_happenings.*', MinistryHappeningsHandler),
  ('/alumni/past_events.*', PastEventsHandler),
  ('/alumni/donate.*', DonateHandler),
  ], debug=True)
