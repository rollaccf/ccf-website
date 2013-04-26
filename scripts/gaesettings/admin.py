from google.appengine.ext import webapp
from scripts import BaseHandler, FormHandler
from . import BaseSetting
from wtforms.ext.appengine.db import model_form
from wtforms.form import Form
from wtforms.fields import *

class NewSettingForm(Form):
    Name=TextField("Name")
    Value=TextField("Value")
    ValueType=SelectField('Value Type',
        choices=[
            ('float', 'Float'),
            ('int', 'Int'),
            ('string', 'String'),
        ],
    )
    Catagory=TextField("Catagory")
    DisplayName=TextField()
    Documentation=TextAreaField()
    ReadOnly=BooleanField("ReadOnly")


class AdminHandler(FormHandler):
    def get(self):
        self.generate_forms([('new_setting_form', NewSettingForm)])
        self.template_vars['existing_settings'] = BaseSetting.query()
        # edit items
        # delete items
        self.render_template("admin/gaesettings.html", use_cache=False)

    def post(self):
        self.process_forms([('new_setting_form', NewSettingForm, self.create_new_setting)])
        self.redirect("/admin/gaesettings")


    def create_new_setting(self, data):
        pass


application = webapp.WSGIApplication([
  ('/admin/gaesettings.*', AdminHandler),
  ], debug=BaseHandler.debug)
