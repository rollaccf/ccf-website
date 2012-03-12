from google.appengine.ext import webapp
from scripts.main import BaseHandler
from scripts.gaesessions import get_current_session
from scripts.database_models import HousingApplication
from wtforms.ext.appengine.db import model_form

class CchHandler(BaseHandler):
    def get(self):
        self.render_template("housing/cch.html",
        { 'title':"Christian Campus Fellowship Men's Housing Info",
          'headerText':"CCH Housing Information",
          'HousingSelected':"top-level-dropdown-selected",
        })

class WcchHandler(BaseHandler):
    def get(self):
        self.render_template("housing/wcch.html",
        { 'title':"Christian Campus Fellowship Women's Housing Info",
          'headerText':"WCCH Housing Information",
          'HousingSelected':"top-level-dropdown-selected",
        })

class ApplicationHandler(BaseHandler):
    FormClass = model_form(HousingApplication)

    def get(self):
        session = get_current_session()
        form = self.FormClass(formdata=session.get('housing_application'))
        if session.has_key('housing_application'):
          form.validate()

        self.render_template("housing/application.html",
        { 'title':"Christian Campus Fellowship Housing Application",
          'headerText':"Housing Application",
          'HousingSelected':"top-level-dropdown-selected",
          'form':form,
        })

    def post(self):
        session = get_current_session()
        form = self.FormClass(self.request.POST)
        if form.validate():
          # clear session['housing_application']
          # create database object
          # send email
          pass


        session['housing_application'] = self.request.POST
        self.redirect(self.request.path)


application = webapp.WSGIApplication([
  ('/housing/cch.*', CchHandler),
  ('/housing/wcch.*', WcchHandler),
  ('/housing/application.*', ApplicationHandler),
  ], debug=True)
