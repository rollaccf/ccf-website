from os.path import join
from google.appengine.ext import webapp
from scripts.main import BaseHandler

class MinistryHappeningsHandler(BaseHandler):
    def get(self):
        self.render_template(join("alumni", "ministry_happenings.html"), { 'title':"CCF Alumni", 'headerText':"Ministry Happenings" })

class UpcomingProgressHandler(BaseHandler):
    def get(self):
        self.render_template(join("alumni", "upcoming_progress.html"), { 'title':"CCF Alumni", 'headerText':"Upcoming Progress" })

class PastEventsHandler(BaseHandler):
    def get(self):
        self.render_template(join("alumni", "past_events.html"), { 'title':"CCF Alumni", 'headerText':"Past Events" })

class DonateHandler(BaseHandler):
    def get(self):
        self.render_template(join("alumni", "donate.html"), { 'title':"CCF Alumni", 'headerText':"Donate" })


application = webapp.WSGIApplication([
  ('/alumni/ministry_happenings.*', MinistryHappeningsHandler),
  ('/alumni/upcoming_progress.*', UpcomingProgressHandler),
  ('/alumni/past_events.*', PastEventsHandler),
  ('/alumni/donate.*', DonateHandler),
  ], debug=True)
