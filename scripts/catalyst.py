from google.appengine.ext import webapp
from scripts import BaseHandler
from scripts.database_models.gel_group import GelGroup

class Catalyst_BaseHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
      super(Catalyst_BaseHandler, self).__init__(*args, **kwargs)
      self.template_vars['CatalystSelected'] = "top-level-dropdown-selected"

class GelGroupsHandler(Catalyst_BaseHandler):
    def get_gel_groups(self):
        self.template_vars["GelGroups"] = GelGroup.gql("ORDER BY DayAndTime ASC").fetch(50)

    def get(self):
        self.register_var_function(self.get_gel_groups)
        self.render_template("catalyst/gel_groups.html")

class SemesterSeriesHandler(Catalyst_BaseHandler):
    def get(self):
        self.render_template("catalyst/semester_series.html")

class SermonScheduleHandler(Catalyst_BaseHandler):
    def get(self):
        self.redirect("/catalyst/semester_series", permanent=True)


application = webapp.WSGIApplication([
  ('/catalyst/gel_groups.*', GelGroupsHandler),
  ('/catalyst/semester_series.*', SemesterSeriesHandler),
  ('/catalyst/sermon_schedule.*', SermonScheduleHandler),
  ], debug=BaseHandler.debug)
