import urllib
from google.appengine.api import images
from google.appengine.ext import webapp, ndb
from . import Manage_BaseHandler
from scripts.database_models.staff_position import StaffPosition, StaffPosition_Form


class Manage_StaffPositions_Handler(Manage_BaseHandler):
    def get(self):
        if self.request.get('retry'):
            form = StaffPosition_Form(formdata=self.session.get('new_staff_position'))
            if self.session.has_key('new_staff_position'):
                form.validate()
        elif self.request.get('edit'):
            editKey = self.request.get("edit")
            form = StaffPosition_Form(obj=ndb.Key(urlsafe=editKey).get())
            self.template_vars['isEdit'] = True
        else:
            form = StaffPosition_Form()

        self.template_vars['existingStaffPositions'] = StaffPosition.gql("ORDER BY DisplayOrder ASC").fetch(50)
        self.template_vars['form'] = form

        self.render_template("manage/staff_positions/staff_positions.html")

    def post(self):
        form = StaffPosition_Form(self.request.POST)
        editKey = self.request.get("edit")
        if form.validate():
            if 'new_staff_position' in self.session:
                del self.session['new_staff_position']
            if editKey:
                filled_staff_position = ndb.Key(urlsafe=editKey).get()
                if filled_staff_position == None:
                    self.abort(500, "The student officer you are trying to edit does not exist")
                filled_staff_position.populate(**form.data)
            else:
                filled_staff_position = StaffPosition(**form.data)

            filled_staff_position.Image = images.resize(filled_staff_position.Image, 147, 123)

            if not filled_staff_position.DisplayOrder:
                # TODO: only get DisplayOrder
                # displayOrderObject = GqlQuery("SELECT DisplayOrder FROM StudentOfficer ORDER BY DisplayOrder DESC").get()
                displayOrderObject = StaffPosition.gql("ORDER BY DisplayOrder DESC").get()
                try:
                    filled_staff_position.DisplayOrder = displayOrderObject.DisplayOrder + 1 if displayOrderObject else 1
                except:
                    # if DisplayOrder is None (NoneType + 1 results in a exception)
                    filled_staff_position.DisplayOrder = 1

            filled_staff_position.put()
            self.redirect(self.request.path)
        else:
            self.session['new_staff_position'] = self.request.POST
            self.redirect(self.request.path + '?edit=%s&retry=1' % editKey)


class Manage_StaffPositions_OrderHandler(Manage_BaseHandler):
    def get(self, direction, displayOrderToMove):
        displayOrderToMove = int(displayOrderToMove)
        # I am assuming displayOrder has no duplicates
        FirstObject = StaffPosition.gql("WHERE DisplayOrder = :1", displayOrderToMove).get()
        if direction == 'u':
            SecondObject = StaffPosition.gql("WHERE DisplayOrder < :1 ORDER BY DisplayOrder DESC",
                                              displayOrderToMove).get()
        else:
            SecondObject = StaffPosition.gql("WHERE DisplayOrder > :1 ORDER BY DisplayOrder ASC",
                                              displayOrderToMove).get()
        FirstObject.DisplayOrder, SecondObject.DisplayOrder = SecondObject.DisplayOrder, FirstObject.DisplayOrder
        FirstObject.put()
        SecondObject.put()
        self.redirect('/manage/staff_positions')


class Manage_StaffPositions_DeleteHandler(Manage_BaseHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        ndb.Key(urlsafe=resource).delete()
        self.redirect('/manage/staff_positions')


application = webapp.WSGIApplication([
    ('/manage/staff_positions/order/([ud])/(\d+)', Manage_StaffPositions_OrderHandler),
    ('/manage/staff_positions/delete/([^/]+)', Manage_StaffPositions_DeleteHandler),
    ('/manage/staff_positions.*', Manage_StaffPositions_Handler),
    ], debug=Manage_BaseHandler.debug)
