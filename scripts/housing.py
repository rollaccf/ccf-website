import logging
from google.appengine.ext import webapp
from google.appengine.api.mail import EmailMessage
from scripts import BaseHandler
from scripts.gaesettings import gaesettings
from scripts.database_models.housingapplication import HousingApplication, HousingApplication_Form


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
    def generate_housing_form(self):
        if self.request.get('retry'):
            form = HousingApplication_Form(formdata=self.session.get('housing_application'))
            if self.session.has_key('housing_application'):
                form.validate()
        else:
            form = HousingApplication_Form()
            house = self.request.get('house')
            if house == 'cch':
                form.House.data = "Men's Christian Campus House"
            elif house == 'wcch':
                form.House.data = "Women's Christian Campus House"

        self.template_vars['form'] = form

    def get(self):
        self.register_var_function(self.generate_housing_form)
        self.render_template("housing/application.html", use_cache=False)

    def post(self):
        form = HousingApplication_Form(self.request.POST)
        if form.validate():
            log_msg = "New Application Submitted: {name} [email:{email}, phone:{phone}]"
            log_msg = log_msg.format(name=form.FullName.data, email=form.EmailAddress.data, phone=form.PhoneNumber.data)
            logging.info(log_msg)

            if 'housing_application' in self.session:
                del self.session['housing_application']
            filled_housing_application = HousingApplication(SemesterToBeginIndex=int(form.SemesterToBegin.data),
                                                            HomeAddress=form.HomeAddress, **form.data)
            filled_housing_application.put()

            # send email
            message = EmailMessage()
            if form.House.data == "Men's Christian Campus House":
                message.sender = "CCH Housing Application <admin@rollaccf.org>"
                message.to = gaesettings.HousingApplicationCch_CompletionEmail
                message.subject = "CCH Housing Application (%s)" % form.FullName.data
            else:
                message.sender = "WCCH Housing Application <admin@rollaccf.org>"
                message.to = gaesettings.HousingApplicationWcch_CompletionEmail
                message.subject = "WCCH Housing Application (%s)" % form.FullName.data
            message.html = filled_housing_application.generateHtmlMailMessageBody()
            message.body = filled_housing_application.generatePlainTextMailMessageBody()
            message.send()

            self.session["app-name"] = filled_housing_application.FullName
            self.redirect(self.request.path + "/done")
        else:
            self.session['housing_application'] = self.request.POST
            self.redirect(self.request.path + '?retry=1')


class ApplicationCompletedHandler(Housing_BaseHandler):
    def get(self):
        self.template_vars['app_name'] = self.session.get("app-name")
        self.render_template("housing/application_completion.html", use_cache=False)


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
    ], debug=BaseHandler.debug)
