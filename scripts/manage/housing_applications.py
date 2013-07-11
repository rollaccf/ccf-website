import logging
import datetime
from google.appengine.ext import webapp, ndb
from . import Manage_BaseHandler
from scripts.database_models.housingapplication import HousingApplication, HousingApplicationNote, HousingApplicationNote_Form
from scripts.database_models.housingapplication import get_semester_text_from_index, get_current_semester_index
from wtforms.form import Form
from wtforms import fields


class HousingApplicationFilter(Form):
    DisplayCchHouse = fields.BooleanField(u'Display CCH Applications', default='y')
    DisplayWcchHouse = fields.BooleanField(u'Display WCCH Applications', default='y')
    SortBy = fields.RadioField(u'Sort By',
                        default='-TimeSubmitted',
                        choices=[
                            ('-TimeSubmitted', 'Time Submitted'),
                            ('FullName', 'Full Name'),
                            ('SemesterToBeginIndex', 'Semester To Begin'),
                        ],
    )
    IncludeArchived = fields.BooleanField(u'Include Archived')
    ShowAllSemesters = fields.BooleanField("Show All Semesters", default='')
    Semester1 = fields.BooleanField(get_semester_text_from_index(get_current_semester_index() + 1), default='y')
    Semester2 = fields.BooleanField(get_semester_text_from_index(get_current_semester_index() + 2), default='y')
    Semester3 = fields.BooleanField(get_semester_text_from_index(get_current_semester_index() + 3), default='y')
    Semester4 = fields.BooleanField(get_semester_text_from_index(get_current_semester_index() + 4), default='y')
    TimeStamp = fields.HiddenField()


class Manage_HousingApplications_Handler(Manage_BaseHandler):
    def get(self):
        filterForm = HousingApplicationFilter(self.request.GET)
        filterFormQuery = HousingApplication.query()

        houses = []
        if filterForm.DisplayCchHouse.data:
            # references database_model choice
            houses.append("Men's Christian Campus House")
        if filterForm.DisplayWcchHouse.data:
            # references database_model choice
            houses.append("Women's Christian Campus House")
        filterFormQuery = filterFormQuery.filter(HousingApplication.House.IN(houses))

        if not filterForm.ShowAllSemesters.data:
            semesters = []
            current_semester_index = get_current_semester_index()
            # simplifies 4 if statements into a single for loop
            for semester_num in (1, 2, 3, 4):
                if getattr(filterForm, "Semester{}".format(semester_num)).data:
                    semesters.append(current_semester_index + semester_num)
            filterFormQuery = filterFormQuery.filter(HousingApplication.SemesterToBeginIndex.IN(semesters))

        if not filterForm.IncludeArchived.data:
            filterFormQuery = filterFormQuery.filter(HousingApplication.Archived == False)

        if filterForm.SortBy.data[0] == '-':
            reverse = True
            prop_name = filterForm.SortBy.data[1:]
        else:
            reverse = False
            prop_name = filterForm.SortBy.data
        prop = getattr(HousingApplication, prop_name)
        if reverse:
            filterFormQuery = filterFormQuery.order(-prop)
        else:
            filterFormQuery = filterFormQuery.order(prop)

        #HousingApplication.gql("WHERE House IN :1 AND SemesterToBeginIndex IN :2 AND Archived == :3 ORDER BY :4")

        # get page
        # get cursor
        apps = filterFormQuery.fetch(100)
        # get number of pages

        self.template_vars['applications'] = apps
        self.template_vars['page'] = 2
        self.template_vars['filterForm'] = filterForm

        self.render_template("manage/housing_applications/housing_applications.html")


class Manage_HousingApplication_ArchiveHandler(Manage_BaseHandler):
    def get(self, action, key):
        app = ndb.Key(urlsafe=key).get()
        if action == 'archive':
            app.Archived = True
        else:
            app.Archived = False
        app.put()

class Manage_HousingApplication_LegacyViewHandler(Manage_BaseHandler):
    def get(self):
        logging.debug("/manage/housing_applications/view_housing_application was used")
        self.redirect('/manage/housing_applications/view/%s' % self.request.get('key'), permanent=True)


class Manage_HousingApplication_ViewHandler(Manage_BaseHandler):
    def get(self, key):
        app = ndb.Key(urlsafe=key).get()
        if not app:
            self.abort(404, "The provided key does not reference a housing application.")

        if self.request.get('retry'):
            form = HousingApplicationNote_Form(formdata=self.session.get('housing_application_note'))
            if self.session.has_key('housing_application_note'):
                form.validate()
        else:
            form = HousingApplicationNote_Form()

        notes_query = HousingApplicationNote.gql("WHERE Application = :1 ORDER BY CreationDateTime", app.key)

        self.template_vars['app'] = app
        self.template_vars['notes'] = notes_query.fetch(50)
        self.template_vars['noteForm'] = form

        self.render_template("manage/housing_applications/view_housing_application.html")

    def post(self, key):
        form = HousingApplicationNote_Form(self.request.POST)
        if form.validate():
            if 'housing_application_note' in self.session:
                del self.session['housing_application_note']
            filled_housing_application_note = HousingApplicationNote(**form.data)
            filled_housing_application_note.Application = ndb.Key(urlsafe=key)
            filled_housing_application_note.put()

            self.redirect(self.request.path)
        else:
            self.session['housing_application_note'] = self.request.POST
            self.redirect(self.request.path + '?retry=1')


class Manage_HousingApplication_AcknowledgeHandler(Manage_BaseHandler):
    def get(self, key):
        Application = ndb.Key(urlsafe=key).get()
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
    ], debug=Manage_BaseHandler.debug)
