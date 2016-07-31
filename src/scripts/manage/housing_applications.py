import os
import logging
import csv
import StringIO
import datetime
from google.appengine.ext import webapp, ndb
from . import Manage_BaseHandler
from scripts.database_models.housing_application import HousingApplication, HousingApplicationStageChange
from scripts.database_models.housing_application import HousingApplicationNote, HousingApplicationNote_Form
from scripts.database_models.housing_reference import HousingReference
from scripts.database_models.housing_application import get_semester_text_from_index, get_current_semester_index
from ext.wtforms.form import Form
from ext.wtforms import fields


class Manage_HousingApplications_BaseHandler(Manage_BaseHandler):
    pass


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

    def __init__(self, *args, **kwargs):
        super(HousingApplicationFilter, self).__init__(*args, **kwargs)
        self._ndb_query = None
        self._can_have_results = None

    @property
    def can_have_results(self):
        if self._can_have_results:
            return self._can_have_results
        self._build_ndb_query()
        return self._can_have_results

    @property
    def ndb_query(self):
        if self._ndb_query:
            return self._ndb_query
        self._build_ndb_query()
        return self._ndb_query

    def _build_ndb_query(self):
        filterFormQuery = HousingApplication.query()

        houses = True
        if self.DisplayCchHouse.data and not self.DisplayWcchHouse.data:
            filterFormQuery = filterFormQuery.filter(HousingApplication.House == "Men's Christian Campus House")
        elif self.DisplayWcchHouse.data and not self.DisplayCchHouse.data:
            filterFormQuery = filterFormQuery.filter(HousingApplication.House == "Women's Christian Campus House")
        elif not self.DisplayCchHouse.data and not self.DisplayWcchHouse.data:
            houses = False

        semesters = []
        if not self.ShowAllSemesters.data:
            current_semester_index = get_current_semester_index()
            # simplifies 4 if statements into a single for loop
            for semester_num in (1, 2, 3, 4):
                if getattr(self, "Semester{}".format(semester_num)).data:
                    semesters.append(current_semester_index + semester_num)
            filterFormQuery = filterFormQuery.filter(HousingApplication.SemesterToBeginIndex.IN(semesters))

        if not self.IncludeArchived.data:
            filterFormQuery = filterFormQuery.filter(HousingApplication.Archived == False)

        if self.SortBy.data[0] == '-':
            reverse = True
            prop_name = self.SortBy.data[1:]
        else:
            reverse = False
            prop_name = self.SortBy.data
        prop = getattr(HousingApplication, prop_name)
        if reverse:
            filterFormQuery = filterFormQuery.order(-prop)
        else:
            filterFormQuery = filterFormQuery.order(prop)

        self._ndb_query = filterFormQuery
        self._can_have_results = houses and (semesters or self.ShowAllSemesters.data)


class Manage_HousingApplications_Handler(Manage_HousingApplications_BaseHandler):
    def get(self, page_number=1):
        self.generate_manage_bar()
        if page_number:
            page_number = int(page_number)
            if page_number <= 0:
                page_number = 1
        else:
            page_number = 1
        page_size = 50

        if 'reset_filter' in self.request.GET:
            del self.request.GET['reset_filter']
            del self.session['housing_apps_filter']

        filterForm = HousingApplicationFilter(self.request.GET, **self.session.get('housing_apps_filter', default={}))
        self.session['housing_apps_filter'] = filterForm.data

        filterFormQuery = filterForm.ndb_query

        if filterForm.can_have_results:
            # cannot do fetch_page here because of the IN queries
            apps_count = filterFormQuery.count()
            last_page_number = max(-(-apps_count // page_size), 1)
            if page_number > last_page_number:
                page_number = last_page_number
            apps = filterFormQuery.fetch(page_size, offset=(page_number - 1)*page_size)
        else:
            apps = []
            apps_count = 0

        self.template_vars['applications'] = apps
        self.template_vars['application_count'] = apps_count
        self.template_vars['filterForm'] = filterForm
        self.template_vars['num_stages'] = 5
        self.template_vars['query_string'] = self.request.query_string
        self.template_vars['host'] = os.environ['HTTP_HOST']

        last_page_number = -(-apps_count // page_size)
        url_template = "/manage/housing_applications/{page_number}"
        if self.request.query_string:
            url_template += "?" + self.request.query_string
        if page_number != 1:
            self.template_vars['first_page'] = url_template.format(page_number=1)
            self.template_vars['prev_page'] = url_template.format(page_number=page_number - 1)
        if page_number != last_page_number:
            self.template_vars['next_page'] = url_template.format(page_number=page_number + 1)
            self.template_vars['last_page'] = url_template.format(page_number=last_page_number)
        self.template_vars['current_page'] = page_number
        self.template_vars['total_pages'] = last_page_number

        self.render_template("manage/housing_applications/housing_applications.html")


class Manage_HousingApplication_ArchiveHandler(Manage_HousingApplications_BaseHandler):
    def get(self, action, key):
        app = ndb.Key(urlsafe=key).get()
        if action == 'archive':
            app.Archived = True
        else:
            app.Archived = False
        app.put()


class Manage_HousingApplication_LegacyViewHandler(Manage_HousingApplications_BaseHandler):
    def get(self):
        logging.debug("/manage/housing_applications/view_housing_application was used")
        self.redirect('/manage/housing_applications/view/%s' % self.request.get('key'), permanent=True)


# TODO: escape comments; when saving or when displaying?
class Manage_HousingApplication_ViewHandler(Manage_HousingApplications_BaseHandler):
    def get(self, key):
        self.generate_manage_bar()

        application_key = ndb.Key(urlsafe=key)
        if application_key.kind() != "HousingApplication":
            self.abort(404, "Given key is not of kind 'HousingApplication'")

        housing_application = application_key.get()
        if not housing_application:
            self.abort(404, "The provided key does not reference a housing application.")

        notes_query_string = "WHERE Application = :1 ORDER BY CreationDateTime"
        notes_query = HousingApplicationNote.gql(notes_query_string, housing_application.key)

        if housing_application.HomeChurchReferenceKey:
            self.template_vars['church_reference'] = housing_application.HomeChurchReferenceKey.get()

        if housing_application.OtherReferenceKey:
            self.template_vars['other_reference'] = housing_application.OtherReferenceKey.get()

        self.template_vars['app'] = housing_application
        self.template_vars['notes'] = notes_query
        self.template_vars['noteForm'] = self.generate_form(HousingApplicationNote_Form)
        self.template_vars['host'] = os.environ['HTTP_HOST']
        self.template_vars['num_stages'] = 5

        self.render_template("manage/housing_applications/view_housing_application.html")

    def post(self, key):
        def post_process_model(filled_housing_application_note):
            filled_housing_application_note.Application = ndb.Key(urlsafe=key)

        filled_housingApplication_note = self.process_form(HousingApplicationNote_Form, HousingApplicationNote,
                                                           PostProcessing=post_process_model)
        if filled_housingApplication_note:
            self.redirect(self.request.path)
        else:
            self.redirect(self.request.path + '?edit=%s&retry=1' % self.request.get("edit"))


class Manage_HousingApplication_ReferenceHandler(Manage_HousingApplications_BaseHandler):
    def get(self, ref_type, key):
        self.generate_manage_bar()

        ref_types = {'c': "church", 'o': "other", }

        ndb_key = ndb.Key(urlsafe=key)
        if ndb_key.kind() != "HousingApplication":
            self.abort(404, "Given key is not of the correct type")

        application = ndb_key.get()
        if not application:
            self.abort(404, "Housing application not found")

        if ref_type == 'c':
            self.template_vars['reference_name'] = application.HomeChurchMinisterName
            self.template_vars['filled_reference'] = application.HomeChurchReferenceKey.get()
        elif ref_type == 'o':
            self.template_vars['reference_name'] = application.OtherReferenceName
            self.template_vars['filled_reference'] = application.OtherReferenceKey.get()
        else:
            self.abort(500, "ref_type unknown '{}'".format(ref_type))
        self.template_vars['reference_name'] = self.template_vars['reference_name'].title()

        self.template_vars['applicant_name'] = application.FullName.title()
        if application.House == "Men's Christian Campus House":
            self.template_vars['applicant_gender'] = ("he", "him", "his")
        else:
            self.template_vars['applicant_gender'] = ("she", "her", "her")

        self.template_vars['ref_type'] = ref_types[ref_type]

        self.render_template("manage/housing_applications/view_housing_reference.html")


class Manage_HousingApplication_StageChangeHandler(Manage_HousingApplications_BaseHandler):
    def get(self, new_stage, key):
        application_key = ndb.Key(urlsafe=key)
        if application_key.kind() != "HousingApplication":
            self.abort(404, "key must be of kind 'HousingApplication'")

        application = application_key.get()
        change = HousingApplicationStageChange(NewStage=int(new_stage))
        application.StageChanges.append(change)
        application.put()

        self.redirect("/manage/housing_applications/view/%s" % key)


class Manage_HousingApplications_ExportHandler(Manage_HousingApplications_BaseHandler):
    def get(self):
        filterForm = HousingApplicationFilter(self.request.GET)
        filterFormQuery = filterForm.ndb_query

        field_names = [
            'TimeSubmitted', 'FullName', 'House', 'CurrentGradeLevel', 'DateOfBirth', 'EmailAddress',
            'HomeAddress', 'Archived', 'PhoneNumber', 'ProposedDegree', 'SemesterToBegin', 'Stage',
            'ParentEmail', 'ParentNames', 'ParentPhoneNumber',
            'HomeChurchEmail', 'HomeChurchMinisterName', 'HomeChurchName', 'HomeChurchPhoneNumber',
            'OtherReferenceEmail', 'OtherReferenceName', 'OtherReferencePhoneNumber', 'OtherReferenceRelation',
            'HowAndWhy', 'LeadershipRoles', 'TalentsAndInterests', 'CriminalActivity',
            'MedicalAllergies', 'Medications',
        ]

        csv_file = StringIO.StringIO()
        w = csv.DictWriter(csv_file, field_names, extrasaction="ignore")
        w.writeheader()

        for x in filterFormQuery:
            row = dict(x.to_dict().items() + {"SemesterToBegin": x.SemesterToBegin}.items())
            for item in row:
                if isinstance(row[item], unicode):
                    row[item] = row[item].encode('ascii', 'replace')
            w.writerow(row)

        self.response.write(csv_file.getvalue())

        self.response.headers.add("Content-Type", "text/csv")
        self.response.headers.add("Content-Disposition", "attachment; filename=\"applications_export.csv\"")


application = webapp.WSGIApplication([
    ('/manage/housing_applications/view/([^/]+)', Manage_HousingApplication_ViewHandler),
    ('/manage/housing_applications/ref/(c|o)/([^/]+)', Manage_HousingApplication_ReferenceHandler),
    ('/manage/housing_applications/stage/(\d)/([^/]+)', Manage_HousingApplication_StageChangeHandler),
    ('/manage/housing_applications/view_housing_application.*', Manage_HousingApplication_LegacyViewHandler),
    ('/manage/housing_applications/(archive|unarchive)/([^/]+)', Manage_HousingApplication_ArchiveHandler),
    ('/manage/housing_applications/export', Manage_HousingApplications_ExportHandler),
    ('/manage/housing_applications/?(\d+)?', Manage_HousingApplications_Handler),
    ], debug=Manage_BaseHandler.debug)
