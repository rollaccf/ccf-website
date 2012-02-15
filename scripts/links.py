from os.path import join
from google.appengine.ext import webapp
from scripts.main import BaseHandler

class ResourcesHandler(BaseHandler):
    def get(self):
        self.render_template(join("links", "resources.html"),
          { 'title':"Resources",
            'LinksSelected':"top-level-dropdown-selected",
        })

class SupportingChurchesHandler(BaseHandler):
    def get(self):
        self.render_template(join("links", "supporting_churches.html"),
          { 'title':"CCF Links",
            'LinksSelected':"top-level-dropdown-selected"
        })

application = webapp.WSGIApplication([
  ('/links/resources.*', ResourcesHandler),
  ('/links/supporting_churches.*', SupportingChurchesHandler),
  ], debug=True)
