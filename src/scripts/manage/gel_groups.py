import urllib
from google.appengine.ext import webapp, ndb
from . import Manage_BaseHandler
from scripts.database_models.gel_group import GelGroup, GelGroup_Form


class Manage_GelGroups_Handler(Manage_BaseHandler):
    def get(self):
        self.template_vars['existingGelGroups'] = GelGroup.gql("ORDER BY DayAndTime ASC").fetch(50)
        self.template_vars['form'] = self.generate_form(GelGroup_Form)

        self.render_template("manage/gel_groups/gel_groups.html")


    def post(self):
        filled_gel_group = self.process_form(GelGroup_Form, GelGroup)
        if filled_gel_group:
            self.redirect(self.request.path)
        else:
            self.redirect(self.request.path + '?edit=%s&retry=1' % self.request.get("edit"))


class Manage_GelGroups_DeleteHandler(Manage_BaseHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        ndb.Key(urlsafe=resource).delete()
        self.redirect('/manage/gel_groups')


application = webapp.WSGIApplication([
    ('/manage/gel_groups/delete/([^/]+)', Manage_GelGroups_DeleteHandler),
    ('/manage/gel_groups.*', Manage_GelGroups_Handler),
    ], debug=Manage_BaseHandler.debug)
