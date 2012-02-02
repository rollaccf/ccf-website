from os.path import join
from google.appengine.ext import webapp
from scripts.main import BaseHandler

class CchHandler(BaseHandler):
    def get(self):
        self.render_template(join("housing", "cch.html"), { 'title':"CCF Housing", 'headerText':"CCH Housing Information", 'HousingSelected':"top-level-dropdown-selected" })

class WcchHandler(BaseHandler):
    def get(self):
        self.render_template(join("housing", "wcch.html"), { 'title':"CCF Housing", 'headerText':"WCCH Housing Information", 'HousingSelected':"top-level-dropdown-selected" })

class ApplicationHandler(BaseHandler):
    def get(self):
        self.render_template(join("housing", "application.html"), { 'title':"CCF Housing", 'headerText':"WCCH Housing Application", 'HousingSelected':"top-level-dropdown-selected" })


application = webapp.WSGIApplication([
  ('/housing/cch.*', CchHandler),
  ('/housing/wcch.*', WcchHandler),
  ('/housing/application.*', ApplicationHandler),
  ], debug=True)
