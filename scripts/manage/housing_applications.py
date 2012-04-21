from google.appengine.ext import webapp
from google.appengine.ext.db import GqlQuery
from scripts.main import BaseHandler
from scripts.gaesessions import get_current_session
from scripts.database_models import HousingApplication, HousingApplicationNote
from wtforms.ext.appengine.db import model_form

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
    FormClass = model_form(HousingApplicationNote)

    def get(self):
      session = get_current_session()
      key = self.request.get('key')
      app = HousingApplication.get(key)
      # TODO: error handling for app key

      if self.request.get('retry'):
        form = self.FormClass(formdata=session.get('housing_application_note'))
        if session.has_key('housing_application_note'):
          form.validate()
      else:
        form = self.FormClass()

      self.render_template("manage/housing_applications/view_housing_application.html",
      { 'title':"Manage Housing Applications",
        'app':app,
        'notes':app.notes.fetch(30),# TODO: add ordering
        'noteForm':form,
      })

    def post(self):
      session = get_current_session()
      key = self.request.get('key')
      form = self.FormClass(self.request.POST)
      if form.validate():
        if 'housing_application_note' in session:
          del session['housing_application_note']
        filled_housing_application_note = HousingApplicationNote(**form.data)
        filled_housing_application_note.Application = HousingApplication.get(key)
        filled_housing_application_note.put()

        self.redirect(self.request.path + '?key=' + key)
      else:
        session['housing_application_note'] = self.request.POST
        self.redirect(self.request.path + '?retry=1&key=' + key)


application = webapp.WSGIApplication([
  ('/manage/housing_applications/view_housing_application.*', ManageViewHousingApplicationHandler),
  ('/manage/housing_applications.*', ManageHousingApplicationsHandler),
  ], debug=True)
