import urllib
from google.appengine.ext import webapp, ndb
from scripts.admin import Admin_BaseHandler
from scripts.database_models.gae_setting import BaseSetting, FloatSetting, IntSetting, StringSetting, NewSetting_Form


class Admin_GaeSettings_Handler(Admin_BaseHandler):
    def get(self):
        if self.request.get('retry'):
            form = NewSetting_Form(formdata=self.session.get('new_gae_setting'))
            if self.session.has_key('new_gae_setting'):
                form.validate()
        elif self.request.get('edit'):
            editKey = self.request.get("edit")
            edit_obj = ndb.Key(urlsafe=editKey).get()
            form = NewSetting_Form(obj=edit_obj)
            form.Name.data = edit_obj.key.id()
            form.ValueType.data = edit_obj.Value.__class__.__name__
            self.template_vars['editKey'] = editKey
        else:
            form = NewSetting_Form()

        self.template_vars['existing_settings'] = BaseSetting.query()
        self.template_vars['new_setting_form'] = form

        self.render_template("admin/gae_settings.html")


    def post(self):
        form = NewSetting_Form(self.request.POST)
        editKey = self.request.get("edit")
        if form.validate():
            form_data = form.data
            form_data['Value'] = {
                'int':int,
                'float':float,
                'unicode':str,}[form.ValueType.data](form_data['Value'])
            del form_data['Name']
            del form_data['ValueType']

            if 'new_gae_setting' in self.session:
                del self.session['new_gae_setting']
            if editKey:
                filled_gae_setting = ndb.Key(urlsafe=editKey).get()
                if filled_gae_setting == None:
                    self.abort(500, "The student officer you are trying to edit does not exist")
                filled_gae_setting.populate(**form_data)
            else:
                model_type = {
                    'int':IntSetting,
                    'float':FloatSetting,
                    'unicode':StringSetting,
                    }[form.ValueType.data]
                filled_gae_setting = model_type(id=form.Name.data, **form_data)

            filled_gae_setting.put()
            self.redirect(self.request.path)
        else:
            self.session['new_gae_setting'] = self.request.POST
            self.redirect(self.request.path + '?edit=%s&retry=1' % editKey)


class Admin_GaeSettings_DeleteHandler(Admin_BaseHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        ndb.Key(urlsafe=resource).delete()
        self.redirect('/admin/gae_settings')


application = webapp.WSGIApplication([
  ('/admin/gae_settings/delete/([^/]+)', Admin_GaeSettings_DeleteHandler),
  ('/admin/gae_settings.*', Admin_GaeSettings_Handler),
  ], debug=Admin_BaseHandler.debug)
