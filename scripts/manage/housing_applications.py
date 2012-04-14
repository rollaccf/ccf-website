from google.appengine.ext import webapp
from google.appengine.ext.db import GqlQuery
from scripts.main import BaseHandler
from scripts.database_models import HousingApplication

class ManageHousingApplicationsHandler(BaseHandler):
    def get(self):
      # get page
      # get cursor
      #
      query = HousingApplication.gql("ORDER BY TimeSubmitted")
      apps = query.fetch(50)
      # get apps
      # get pages
      self.render_template("manage/housing_applications/housing_applications.html",
      { 'title':"Manage Housing Applications",
        'applications':apps,
        'page':2,
      })

class ManageViewHousingApplicationHandler(BaseHandler):
    def get(self):
      key = self.request.get('key')
      app = HousingApplication.get(key)
      # TODO: error handling
      # get comments
      self.render_template("manage/housing_applications/view_housing_application.html",
      { 'title':"Manage Housing Applications",
        'app':app,
      })

    def post(self):
      # save comments
      pass

application = webapp.WSGIApplication([
  ('/manage/housing_applications/view_housing_application.*', ManageViewHousingApplicationHandler),
  ('/manage/housing_applications.*', ManageHousingApplicationsHandler),
  ], debug=True)
