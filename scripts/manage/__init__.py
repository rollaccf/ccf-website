from os.path import join
from google.appengine.ext import webapp
from scripts.main import BaseHandler

class ManageHandler(BaseHandler):
    def get(self):
      self.render_template(join("manage", "manage.html"), { 'title':"CCF Website Management", })


application = webapp.WSGIApplication([
  ('/manage.*', ManageHandler),
  ], debug=True)