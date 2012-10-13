import urllib
from google.appengine.ext import webapp
from scripts.main import BaseHandler
from scripts.gaesessions import get_current_session
from scripts.database_models.gel_group import GelGroup, GelGroup_Form



class Manage_GelGroups_Handler(BaseHandler):
    def get(self):
      session = get_current_session()

      if self.request.get('retry'):
        form = GelGroup_Form(formdata=session.get('new_gel_group'))
        if session.has_key('new_gel_group'):
          form.validate()
      elif self.request.get('edit'):
        editKey = self.request.get("edit")
        form = GelGroup_Form(obj=GelGroup.get(editKey))
      else:
        form = GelGroup_Form()

      self.render_template("manage/gel_groups/gel_groups.html",
      { 'existingGelGroups':GelGroup.gql("ORDER BY DayAndTime ASC").fetch(50),
        'form':form,
      },use_cache=False)

    def post(self):
      session = get_current_session()
      form = GelGroup_Form(self.request.POST)
      editKey = self.request.get("edit")
      if form.validate():
        if 'new_gel_group' in session:
          del session['new_gel_group']
        if editKey:
          filled_gel_group = GelGroup.get(editKey)
          if filled_gel_group == None:
            self.abort(500, "The gel group you are trying to edit does not exist")
          filled_gel_group.Update(form.data)
        else:
          filled_gel_group = GelGroup(**form.data)


        filled_gel_group.put()
        self.redirect(self.request.path)
      else:
        session['new_gel_group'] = self.request.POST
        self.redirect(self.request.path + '?edit=%s&retry=1' % editKey)

class Manage_GelGroups_DeleteHandler(BaseHandler):
  def get(self, resource):
    resource = str(urllib.unquote(resource))
    gelGroup = GelGroup.get(resource)
    gelGroup.delete()
    self.redirect('/manage/gel_groups')

application = webapp.WSGIApplication([
  ('/manage/gel_groups/delete/([^/]+)', Manage_GelGroups_DeleteHandler),
  ('/manage/gel_groups.*', Manage_GelGroups_Handler),
  ], debug=BaseHandler.debug)
