from google.appengine.ext import webapp
from scripts.main import BaseHandler

class GelGroupsHandler(BaseHandler):
    def get(self):
        self.render_template("catalyst/gel_groups.html",
        { 'title':"Gel Groups",
          'headerText':"Gel Groups",
          'CatalystSelected':"top-level-dropdown-selected",
        })

class SermonScheduleHandler(BaseHandler):
    def get(self):
        self.render_template("catalyst/sermon_schedule.html",
        { 'title':"CCF Sermon Schedule",
          'headerText':"CCF Sermon Schedule",
          'CatalystSelected':"top-level-dropdown-selected",
        })

class SermonArchiveHandler(BaseHandler):
    def get(self):
        self.render_template("catalyst/sermon_archive.html",
        { 'title':"CCF Sermon Archive",
          'headerText':"CCF Sermon Archive",
          'CatalystSelected':"top-level-dropdown-selected",
        })


application = webapp.WSGIApplication([
  ('/catalyst/gel_groups.*', GelGroupsHandler),
  ('/catalyst/sermon_archive.*', SermonArchiveHandler),
  ('/catalyst/sermon_schedule.*', SermonScheduleHandler),
  ], debug=True)
