import urllib
from google.appengine.ext import webapp, ndb
from scripts.main import BaseHandler
from scripts.database_models.gel_group import GelGroup, GelGroup_Form


class Manage_GelGroups_Handler(BaseHandler):
    def get(self):
        if self.request.get('retry'):
            form = GelGroup_Form(formdata=self.session.get('new_gel_group'))
            if self.session.has_key('new_gel_group'):
                form.validate()
        elif self.request.get('edit'):
            editKey = self.request.get("edit")
            form = GelGroup_Form(obj=ndb.Key(urlsafe=editKey).get())
            self.template_vars['edit'] = True
        else:
            form = GelGroup_Form()

        self.template_vars['existingGelGroups'] = GelGroup.gql("ORDER BY DayAndTime ASC").fetch(50)
        self.template_vars['form'] = form

        self.render_template("manage/gel_groups/gel_groups.html", use_cache=False)

    def post(self):
        form = GelGroup_Form(self.request.POST)
        editKey = self.request.get("edit")
        if form.validate():
            if 'new_gel_group' in self.session:
                del self.session['new_gel_group']
            if editKey:
                filled_gel_group = ndb.Key(urlsafe=editKey).get()
                if filled_gel_group == None:
                    self.abort(500, "The gel group you are trying to edit does not exist")
                filled_gel_group.populate(**form.data)
            else:
                filled_gel_group = GelGroup(**form.data)

            filled_gel_group.put()
            self.redirect(self.request.path)
        else:
            self.session['new_gel_group'] = self.request.POST
            self.redirect(self.request.path + '?edit=%s&retry=1' % editKey)


class Manage_GelGroups_DeleteHandler(BaseHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        ndb.Key(urlsafe=resource).delete()
        self.redirect('/manage/gel_groups')


application = webapp.WSGIApplication([
    ('/manage/gel_groups/delete/([^/]+)', Manage_GelGroups_DeleteHandler),
    ('/manage/gel_groups.*', Manage_GelGroups_Handler),
    ], debug=BaseHandler.debug)
