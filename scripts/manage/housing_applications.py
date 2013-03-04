import datetime
from google.appengine.ext import webapp
from scripts.main import BaseHandler
from scripts.database_models.housingapplication import *
from wtforms.ext.appengine.db import model_form
from wtforms.form import Form
from wtforms.fields import *

class HousingApplicationFilter(Form):
    DisplayCchHouse = BooleanField(u'Display CCH Applications', default='y')
    DisplayWcchHouse = BooleanField(u'Display WCCH Applications', default='y')
    SortBy = RadioField(u'Sort By',
      default='-TimeSubmitted',
      choices=[
        ('-TimeSubmitted', 'Time Submitted'),
        ('-FullName', 'Full Name'),
        ('SemesterToBeginIndex', 'Semester To Begin'),
      ],
    )
    IncludeArchived = BooleanField(u'Include Achived')
    ShowAllSemesters = BooleanField("Show All Semesters", default='')
    Semester1 = BooleanField(get_semester_text_from_index(get_current_semester_index() + 1), default='y')
    Semester2 = BooleanField(get_semester_text_from_index(get_current_semester_index() + 2), default='y')
    Semester3 = BooleanField(get_semester_text_from_index(get_current_semester_index() + 3), default='y')
    Semester4 = BooleanField(get_semester_text_from_index(get_current_semester_index() + 4), default='y')
    TimeStamp = HiddenField()

class Manage_HousingApplications_Handler(BaseHandler):
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

      if not filterForm.ShowAllSemesters.data:
        semesters = []
        current_semester_index = get_current_semester_index()
        # simplifies 4 if statments into a single for loop
        for semester_num in (1, 2, 3, 4):
          if getattr(filterForm, "Semester{}".format(semester_num)).data:
            semesters.append(current_semester_index + semester_num)
        query.filter("SemesterToBeginIndex IN", semesters)

      if not filterForm.IncludeArchived.data:
        query.filter("Archived =", False)

      query.order(filterForm.SortBy.data)

      # get page
      # get cursor
      apps = query.fetch(50)
      # get number of pages

      self.template_vars['applications'] = apps
      self.template_vars['page'] = 2
      self.template_vars['filterForm'] = filterForm

      self.render_template("manage/housing_applications/housing_applications.html", use_cache=False)

class Manage_HousingApplication_ArchiveHandler(BaseHandler):
    def get(self, type, key):
      try:
        app = HousingApplication.get(key)
        if type == 'archive':
            app.Archived = True
        else:
            app.Archived = False
        app.put()
      except:
        pass

class Manage_HousingApplication_LegacyViewHandler(BaseHandler):
    def get(self):
      logging.debug("/manage/housing_applications/view_housing_application was used")
      self.redirect('/manage/housing_applications/view/%s' % self.request.get('key'), permanent=True)

class Manage_HousingApplication_ViewHandler(BaseHandler):
    FormClass = model_form(HousingApplicationNote)

    def get(self, key):
      app = HousingApplication.get(key)
      # TODO: error handling for app key

      if self.request.get('retry'):
        form = self.FormClass(formdata=self.session.get('housing_application_note'))
        if self.session.has_key('housing_application_note'):
          form.validate()
      else:
        form = self.FormClass()

      notes_query = app.notes
      notes_query.order("CreationDateTime")

      self.template_vars['app'] = app
      self.template_vars['notes'] = notes_query.fetch(50)
      self.template_vars['noteForm'] = form

      self.render_template("manage/housing_applications/view_housing_application.html", use_cache=False)

    def post(self, key):
      form = self.FormClass(self.request.POST)
      if form.validate():
        if 'housing_application_note' in self.session:
          del self.session['housing_application_note']
        filled_housing_application_note = HousingApplicationNote(**form.data)
        filled_housing_application_note.Application = HousingApplication.get(key)
        filled_housing_application_note.put()

        self.redirect(self.request.path)
      else:
        self.session['housing_application_note'] = self.request.POST
        self.redirect(self.request.path + '?retry=1')

class Manage_HousingApplication_AcknowledgeHandler(BaseHandler):
    def get(self, key):
        Application = HousingApplication.get(key)
        if Application.Acknowledged != True:
            Application.Acknowledged = True
            Application.TimeAcknowledged = datetime.datetime.utcnow()
            Application.AcknowledgedBy = self.current_user
            Application.put()

        self.redirect("/manage/housing_applications/view/%s" % key)


application = webapp.WSGIApplication([
  ('/manage/housing_applications/view/([^/]+)', Manage_HousingApplication_ViewHandler),
  ('/manage/housing_applications/acknowledge/([^/]+)', Manage_HousingApplication_AcknowledgeHandler),
  ('/manage/housing_applications/view_housing_application.*', Manage_HousingApplication_LegacyViewHandler),
  ('/manage/housing_applications/(archive|unarchive)/([^/]+)', Manage_HousingApplication_ArchiveHandler),
  ('/manage/housing_applications.*', Manage_HousingApplications_Handler),
  ], debug=BaseHandler.debug)
