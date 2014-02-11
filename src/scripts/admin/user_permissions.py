import urllib
from google.appengine.ext import webapp, ndb
from scripts.admin import Admin_BaseHandler
from scripts.database_models.user_permission import UserPermission, UserPermission_Form


class Admin_UserPermissions_Handler(Admin_BaseHandler):
    def get(self):
        self.template_vars['user_permissions'] = UserPermission.query()
        self.template_vars['form'] = self.generate_form(UserPermission_Form)

        self.render_template("admin/user_permissions.html")

    def post(self):
        filled_user_permission = self.process_form(UserPermission_Form, UserPermission)
        if filled_user_permission:
            self.redirect(self.request.path)
        else:
            self.redirect(self.request.path + '?edit=%s&retry=1' % self.request.get("edit"))


class Admin_UserPermissions_DeleteHandler(Admin_BaseHandler):
    def get(self, urlsafe_key):
        urlsafe_key = str(urllib.unquote(urlsafe_key))
        key = ndb.Key(urlsafe=urlsafe_key)
        if key.kind() == 'UserPermission':
            key.delete()
        else:
            self.abort(400, "Can only delete kind 'UserPermission'")
        self.redirect('/admin/user_permissions')


application = webapp.WSGIApplication([
  ('/admin/user_permissions/delete/([^/]+)', Admin_UserPermissions_DeleteHandler),
  ('/admin/user_permissions.*', Admin_UserPermissions_Handler),
  ], debug=Admin_BaseHandler.debug)
