from google.appengine.ext import webapp
from google.appengine.api.mail import EmailMessage
from scripts import BaseHandler
from scripts.gaesessions import get_current_session
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
        session = get_current_session()

        if self.request.get('retry'):
          form = HousingApplication_Form(formdata=session.get('housing_application'))
          if session.has_key('housing_application'):
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
        session = get_current_session()
        form = HousingApplication_Form(self.request.POST)
        if form.validate():
          if 'housing_application' in session:
            del session['housing_application']
          filled_housing_application = HousingApplication(SemesterToBeginIndex=int(form.SemesterToBegin.data), **form.data)
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
          message.html = filled_housing_application.generateHtmlMailMessageBody();
          message.body = filled_housing_application.generatePlainTextMailMessageBody();
          message.send()

          session["app-name"] = filled_housing_application.FullName
          self.redirect(self.request.path + "/done")
        else:
          session['housing_application'] = self.request.POST
          self.redirect(self.request.path + '?retry=1')

class ApplicationCompletedHandler(Housing_BaseHandler):
    def get(self):
        session = get_current_session()
        self.template_vars['app_name'] = session.get("app-name")
        self.render_template("housing/application_completion.html", use_cache=False)

class InfoHandler(Housing_BaseHandler):
    def get(self):
        self.render_template("housing/info.html")


application = webapp.WSGIApplication([
  ('/housing/info.*', InfoHandler),
  ('/housing/cch.*', CchHandler),
  ('/housing/wcch.*', WcchHandler),
  ('/housing/application/done.*', ApplicationCompletedHandler),
  ('/housing/application.*', ApplicationHandler),
  ], debug=BaseHandler.debug)
