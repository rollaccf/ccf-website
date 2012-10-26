from google.appengine.ext import webapp
from scripts import BaseHandler

class Resources_BaseHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
      super(Resources_BaseHandler, self).__init__(*args, **kwargs)
      self.template_vars['LinksSelected'] = "top-level-dropdown-selected"

class ResourcesHandler(Resources_BaseHandler):
    def get(self):
        self.render_template("resources/resources.html")


application = webapp.WSGIApplication([
  ('/resources.*', ResourcesHandler),
  ], debug=BaseHandler.debug)
