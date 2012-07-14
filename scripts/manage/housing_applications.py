from google.appengine.ext import webapp
from scripts.main import BaseHandler
from scripts.gaesessions import get_current_session
from scripts.database_models import HousingApplication, HousingApplicationNote
from wtforms.ext.appengine.db import model_form
from wtforms.form import Form
from wtforms.fields import *

class HousingApplicationFilter(Form):
    DisplayCchHouse = BooleanField(u'Display CCH Applications', default='y')
    DisplayWcchHouse = BooleanField(u'Display WCCH Applications', default='y')
    SortBy = SelectField(u'Sort By',
      default='TimeSubmitted',
      choices=[
        ('TimeSubmitted', 'Time Submitted'),
        ('FullName', 'Full Name'),
        ('DateOfBirth', 'Date Of Birth'),
        ('CurrentGradeLevel', 'Current Grade Level'),
        ('ProposedDegree', 'Proposed Degree'),
        ('SemesterToBegin', 'Semester To Begin'),
      ],
    )
    SortDirection = RadioField(u'Sort Direction', choices=[('asc', 'Ascending'), ('desc', 'Descending')], default='desc',)
    ExcludePastSemesters = BooleanField(u'Exclude Past Semesters')
    # TODO: StartSemester checkbox array to only display certain start semesters

class ManageHousingApplicationsHandler(BaseHandler):
    def get(self):
      filterForm = HousingApplicationFilter(self.request.GET)
      query = HousingApplication.all()

      houses = []
      if filterForm.DisplayCchHouse.data:
        # references database_model choice
        houses.append("Men's Christian Campus House")
      if filterForm.DisplayWcchHouse.data:
        # references database_model choice
        houses.append("Women's Christian Campus House")
      query.filter("House IN", houses)

      if filterForm.SortDirection.data == "desc":
        query.order(filterForm.SortBy.data)
      else:
        query.order("-"+filterForm.SortBy.data)

      if filterForm.ExcludePastSemesters.data:
        # TODO: Add ExcludePastSemesters filter
        # the problem with this is, SemesterToBegin is a string.
        # It is hard to do an inequality against a string
        pass

      # get page
      # get cursor
      apps = query.fetch(50)
      # get number of pages
      self.render_template("manage/housing_applications/housing_applications.html",
      { 'title':"Manage Housing Applications",
        'applications':apps,
        'page':2,
        'filterForm':filterForm,
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
  ], debug=BaseHandler.debug)
