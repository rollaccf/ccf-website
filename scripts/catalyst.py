from os.path import join
from google.appengine.ext import webapp
from scripts.main import BaseHandler

class SermonScheduleHandler(BaseHandler):
    def get(self):
        self.render_template(join("catalyst", "sermon_schedule.html"), { 'title':"CCF Sermon Schedule", 'headerText':"CCF Sermon Schedule" })

class SermonArchiveHandler(BaseHandler):
    def get(self):
        self.render_template(join("catalyst", "sermon_archive.html"), { 'title':"CCF Sermon Archive", 'headerText':"CCF Sermon Archive" })


application = webapp.WSGIApplication([
  ('/catalyst/sermon_archive.*', SermonArchiveHandler),
  ('/catalyst/sermon_schedule.*', SermonScheduleHandler),
  ], debug=True)
