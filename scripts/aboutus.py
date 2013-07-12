from google.appengine.ext import webapp
from scripts import BaseHandler
from scripts.database_models.staff_position import StaffPosition
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
    def get(self):
        self.template_vars['StaffPositions'] = StaffPosition.gql("ORDER BY DisplayOrder ASC")
        self.template_vars['studentOfficers'] = StudentOfficer.gql("ORDER BY DisplayOrder ASC").fetch(50)
        self.render_template("aboutus/staff.html")


application = webapp.WSGIApplication([
    ('/aboutus/beliefs.*', BeliefsHandler),
    ('/aboutus/history.*', HistoryHandler),
    ('/aboutus/location.*', LocationHandler),
    ('/aboutus/staff.*', StaffHandler),
    ], debug=BaseHandler.debug)
