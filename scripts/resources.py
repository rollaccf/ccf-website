from google.appengine.ext import webapp
from scripts.main import BaseHandler

class ResourcesHandler(BaseHandler):
    def get(self):
        self.render_template("resources/resources.html",
        { 'title':"Resources",
          'LinksSelected':"top-level-dropdown-selected",
        })

application = webapp.WSGIApplication([
  ('/resources.*', ResourcesHandler),
  ], debug=BaseHandler.debug)
