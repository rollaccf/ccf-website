from google.appengine.ext import webapp
from scripts import BaseHandler
from scripts.database_models.student_officer import StudentOfficer

class AboutUs_BaseHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(AboutUs_BaseHandler, self).__init__(*args, **kwargs)
        self.template_vars['AboutUsSelected'] = "top-level-dropdown-selected"

class BeliefsHandler(AboutUs_BaseHandler):
    def get(self):
        self.render_template("aboutus/beliefs.html")

class HistoryHandler(AboutUs_BaseHandler):
    def get(self):
        self.render_template("aboutus/history.html")

class LocationHandler(AboutUs_BaseHandler):
    def get(self):
        self.render_template("aboutus/location.html")

class StaffHandler(AboutUs_BaseHandler):
    def get_StudentOfficers(self):
        self.template_vars['studentOfficers'] = StudentOfficer.gql("ORDER BY DisplayOrder ASC").fetch(50)

    def get(self):
        self.register_var_function(self.get_StudentOfficers)
        self.render_template("aboutus/staff.html")


application = webapp.WSGIApplication([
  ('/aboutus/beliefs.*', BeliefsHandler),
  ('/aboutus/history.*', HistoryHandler),
  ('/aboutus/location.*', LocationHandler),
  ('/aboutus/staff.*', StaffHandler),
  ], debug=BaseHandler.debug)
