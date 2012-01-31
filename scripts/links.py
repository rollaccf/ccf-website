from os.path import join
from google.appengine.ext import webapp
from scripts.main import BaseHandler

class LinksHandler(BaseHandler):
    def get(self):
        self.render_template(join("links", "links.html"), { 'title':"CCF Links", 'headerText':"Links" })


application = webapp.WSGIApplication([
  ('/links.*', LinksHandler),
  ], debug=True)
