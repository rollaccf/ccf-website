import urllib
from google.appengine.api import images
from google.appengine.ext import webapp, ndb
from scripts.main import BaseHandler
from scripts.database_models.student_officer import StudentOfficer, StudentOfficer_Form



class Manage_StudentOfficers_Handler(BaseHandler):
    def get(self):
      if self.request.get('retry'):
        form = StudentOfficer_Form(formdata=self.session.get('new_student_officer'))
        if self.session.has_key('new_student_officer'):
          form.validate()
      elif self.request.get('edit'):
        editKey = self.request.get("edit")
        form = StudentOfficer_Form(obj=ndb.Key(urlsafe=editKey).get())
      else:
        form = StudentOfficer_Form()

      self.template_vars['existingStudentOfficers'] = StudentOfficer.gql("ORDER BY DisplayOrder ASC").fetch(50)
      self.template_vars['form'] = form

      self.render_template("manage/student_officers/student_officers.html", use_cache=False)

    def post(self):
      form = StudentOfficer_Form(self.request.POST)
      editKey = self.request.get("edit")
      if form.validate():
        if 'new_student_officer' in self.session:
          del self.session['new_student_officer']
        if editKey:
          filled_student_officer = ndb.Key(urlsafe=editKey).get()
          if filled_student_officer == None:
            self.abort(500, "The student officer you are trying to edit does not exist")
          filled_student_officer.Update(form.data)
        else:
          filled_student_officer = StudentOfficer(**form.data)

        filled_student_officer.Image = images.resize(filled_student_officer.Image, 100, 196)

        if not filled_student_officer.DisplayOrder:
          # TODO: only get DisplayOrder
          # displayOrderObject = GqlQuery("SELECT DisplayOrder FROM SudentOfficer ORDER BY DisplayOrder DESC").get()
          displayOrderObject = StudentOfficer.gql("ORDER BY DisplayOrder DESC").get()
          try:
            filled_student_officer.DisplayOrder = displayOrderObject.DisplayOrder + 1 if displayOrderObject else 1
          except:
            # if DisplayOrder is None (NoneType + 1 results in a exception)
            filled_student_officer.DisplayOrder = 1

        filled_student_officer.put()
        self.redirect(self.request.path)
      else:
        self.session['new_student_officer'] = self.request.POST
        self.redirect(self.request.path + '?edit=%s&retry=1' % editKey)

class Manage_StudentOfficers_OrderHandler(BaseHandler):
  def get(self, direction, displayOrderToMove):
    displayOrderToMove = int(displayOrderToMove)
    # I am assuming displayOrder has no duplicates
    FirstObject = StudentOfficer.gql("WHERE DisplayOrder = :1", displayOrderToMove).get()
    if direction == 'u':
      SecondObject = StudentOfficer.gql("WHERE DisplayOrder < :1 ORDER BY DisplayOrder DESC", displayOrderToMove).get()
    else:
      SecondObject = StudentOfficer.gql("WHERE DisplayOrder > :1 ORDER BY DisplayOrder ASC", displayOrderToMove).get()
    FirstObject.DisplayOrder, SecondObject.DisplayOrder = SecondObject.DisplayOrder, FirstObject.DisplayOrder
    FirstObject.put()
    SecondObject.put()
    self.redirect('/manage/student_officers')

class Manage_StudentOfficers_DeleteHandler(BaseHandler):
  def get(self, resource):
    resource = str(urllib.unquote(resource))
    ndb.Key(urlsafe=resource).delete()
    self.redirect('/manage/student_officers')

application = webapp.WSGIApplication([
  ('/manage/student_officers/order/([ud])/(\d+)', Manage_StudentOfficers_OrderHandler),
  ('/manage/student_officers/delete/([^/]+)', Manage_StudentOfficers_DeleteHandler),
  ('/manage/student_officers.*', Manage_StudentOfficers_Handler),
  ], debug=BaseHandler.debug)
