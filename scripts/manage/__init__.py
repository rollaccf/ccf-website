from google.appengine.ext import webapp
from scripts.main import BaseHandler

class ManageHandler(BaseHandler):
    def get(self):
        self.render_template("manage/manage.html")


application = webapp.WSGIApplication([
  ('/manage.*', ManageHandler),
  ], debug=BaseHandler.debug)
