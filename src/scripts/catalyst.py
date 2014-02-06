import logging
from google.appengine.ext import webapp
from scripts import BaseHandler
from scripts.database_models.gel_group import GelGroup
from scripts.database_models.semester_series import SemesterSeries
from scripts.database_models.top_ten import TopTen


class Catalyst_BaseHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(Catalyst_BaseHandler, self).__init__(*args, **kwargs)
        self.template_vars['CatalystSelected'] = "top-level-dropdown-selected"


class GelGroupsHandler(Catalyst_BaseHandler):
    def get(self):
        self.template_vars["GelGroups"] = GelGroup.gql("ORDER BY DayAndTime ASC").fetch(50)
        self.render_template("catalyst/gel_groups.html")


class SemesterSeriesHandler(Catalyst_BaseHandler):
    def get(self):
        self.template_vars["semester_series"] = SemesterSeries.query().order(-SemesterSeries.CreationDateTime).get()
        self.render_template("catalyst/semester_series.html")


class SermonScheduleHandler(Catalyst_BaseHandler):
    def get(self):
        logging.debug("/catalyst/sermon_schedule was used")
        self.redirect("/catalyst/semester_series", permanent=True)

class TopTenHandler(Catalyst_BaseHandler):
    def get(self):
        self.template_vars["top_tens"] = TopTen.query().order(-TopTen.QuestionDate)
        self.render_template("catalyst/top_ten.html")


application = webapp.WSGIApplication([
    ('/catalyst/gel_groups.*', GelGroupsHandler),
    ('/catalyst/semester_series.*', SemesterSeriesHandler),
    ('/catalyst/sermon_schedule.*', SermonScheduleHandler),
    ('/catalyst/top_ten.*', TopTenHandler),
    ], debug=BaseHandler.debug)
