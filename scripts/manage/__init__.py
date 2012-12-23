from google.appengine.ext import webapp
from scripts.main import BaseHandler

class ManageHandler(BaseHandler):
    def get(self):
        self.render_template("manage/manage.html")

class SetupHandler(BaseHandler):
    def get(self):
        # https://developers.google.com/appengine/articles/update_schema?hl=en

        # Swap the base class of <model> to db.Expando
        # Run this script
        # Swap the base clss back to db.model

        # 22 December 2012
        # update HousingApplication.SemesterToBegin to HousingApplication.SemesterToBeginIndex
	from scripts.database_models.housingapplication import HousingApplication, get_index_from_semester_text
        q = HousingApplication.all()
        for app in q:
            self.response.write("{}<br />".format(app.SemesterToBegin))
            app.SemesterToBeginIndex = get_index_from_semester_text(app.SemesterToBegin)
          # del app.SemesterToBegin


application = webapp.WSGIApplication([
  ('/manage/setup', SetupHandler),
  ('/manage.*', ManageHandler),
  ], debug=BaseHandler.debug)
