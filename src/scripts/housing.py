import logging
from google.appengine.ext import webapp, ndb
from google.appengine.api.mail import EmailMessage
from scripts import BaseHandler
from scripts.database_models.housing_application import HousingApplication, HousingApplication_Form
from scripts.database_models.housing_application import HousingApplicationNote, HousingApplicationNote_Form


class Housing_BaseHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(Housing_BaseHandler, self).__init__(*args, **kwargs)
        self.template_vars['HousingSelected'] = "top-level-dropdown-selected"


class CchHandler(Housing_BaseHandler):
    def get(self):
        self.render_template("housing/cch.html")


class WcchHandler(Housing_BaseHandler):
    def get(self):
        self.render_template("housing/wcch.html")


class ApplicationHandler(Housing_BaseHandler):
    def __init__(self, *args, **kwargs):
        super(ApplicationHandler, self).__init__(*args, **kwargs)
        self.use_cache = False

    def get(self):
        form = self.generate_form(HousingApplication_Form)
        if not self.request.get('retry'):
            house = self.request.get('house')
            if house == 'cch':
                form.House.data = "Men's Christian Campus House"
            elif house == 'wcch':
                form.House.data = "Women's Christian Campus House"
        self.template_vars['form'] = form

        self.render_template("housing/application.html")

    def post(self):
        def pre_process_form_data(form_data):
            form_data['SemesterToBeginIndex'] = int(form_data['SemesterToBegin'])
            del form_data['SemesterToBegin']
            form_data['HomeAddress'] = "{address}, {city}, {state}, {zip}".format(
                address=form_data['SplitHomeAddress'], city=form_data['SplitHomeCity'],
                state=form_data['SplitHomeState'], zip=form_data['SplitHomeZip'])
            del form_data['SplitHomeAddress']
            del form_data['SplitHomeCity']
            del form_data['SplitHomeState']
            del form_data['SplitHomeZip']

        filled_housing_application = self.process_form(HousingApplication_Form, HousingApplication,
                                                       PreProcessing=pre_process_form_data)
        if filled_housing_application:
            message = EmailMessage()
            if filled_housing_application.House == "Men's Christian Campus House":
                message.sender = "CCH Housing Application <admin@rollaccf.org>"
                message.to = self.settings.HousingApplicationCch_CompletionEmail
                message.subject = "CCH Housing Application (%s)" % filled_housing_application.FullName
            else:
                message.sender = "WCCH Housing Application <admin@rollaccf.org>"
                message.to = self.settings.HousingApplicationWcch_CompletionEmail
                message.subject = "WCCH Housing Application (%s)" % filled_housing_application.FullName
            message.html = filled_housing_application.generateHtmlMailMessageBody()
            message.body = filled_housing_application.generatePlainTextMailMessageBody()
            message.send()

            self.session["app-name"] = filled_housing_application.FullName
            self.redirect(self.request.path + "/done")
        else:
            self.redirect(self.request.path + '?edit=%s&retry=1' % self.request.get("edit"))


class ApplicationCompletedHandler(Housing_BaseHandler):
    def __init__(self, *args, **kwargs):
        super(ApplicationCompletedHandler, self).__init__(*args, **kwargs)
        self.use_cache = False

    def get(self):
        self.template_vars['app_name'] = self.session.get("app-name")
        self.render_template("housing/application_completion.html")


class ApplicationComments(Housing_BaseHandler):
    def __init__(self, *args, **kwargs):
        super(ApplicationComments, self).__init__(*args, **kwargs)
        self.use_cache = False
        self.restricted = True

    def get(self, urlsafe_key=None):
        if urlsafe_key:
            ndb_key = ndb.Key(urlsafe=urlsafe_key)
            if ndb_key.kind() != "HousingApplication":
                self.abort(404, "Invalid key")

            self.template_vars['user_email'] = self.current_user.email()
            self.template_vars['applicant_name'] = ndb_key.get().FullName
            self.template_vars['noteForm'] = self.generate_form(HousingApplicationNote_Form)
        else:
            query = HousingApplication.query()
            query = query.filter(HousingApplication.Archived == False)
            mens_applicants = []
            womens_applicants = []
            for housing_application in query:
                data = (housing_application.FullName.title(), housing_application.key.urlsafe())
                if housing_application.House == "Men's Christian Campus House":
                    mens_applicants.append(data)
                else:
                    womens_applicants.append(data)

            self.template_vars['mens_applicants'] = sorted(mens_applicants, key=lambda x: x[0])
            self.template_vars['womens_applicants'] = sorted(womens_applicants, key=lambda x: x[0])
        self.render_template("housing/application_comments.html")

    def post(self, urlsafe_key):
        def post_process_model(filled_housing_application_note):
            filled_housing_application_note.Application = ndb.Key(urlsafe=urlsafe_key)

        filled_housingApplication_note = self.process_form(HousingApplicationNote_Form, HousingApplicationNote,
                                                           PostProcessing=post_process_model)
        if filled_housingApplication_note:
            self.redirect("/housing/comments")
        else:
            self.redirect(self.request.path + '?edit=%s&retry=1' % self.request.get("edit"))


class DetailsHandler(Housing_BaseHandler):
    def get(self):
        self.render_template("housing/details.html")


class InfoHandler(Housing_BaseHandler):
    def get(self):
        logging.debug("/housing/info was used")
        self.redirect("/housing/details", permanent=True)


application = webapp.WSGIApplication([
    ('/housing/info.*', InfoHandler),
    ('/housing/details.*', DetailsHandler),
    ('/housing/cch.*', CchHandler),
    ('/housing/wcch.*', WcchHandler),
    ('/housing/application/done.*', ApplicationCompletedHandler),
    ('/housing/application.*', ApplicationHandler),
    ('/housing/comments/([^/]+)', ApplicationComments),
    ('/housing/comments', ApplicationComments),
    ], debug=BaseHandler.debug)
