from google.appengine.ext import webapp
from scripts.main import BaseHandler

class ManageHandler(BaseHandler):
    def get(self):
        self.render_template("manage/manage.html")

class SetupHandler(BaseHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/plain"
        self.response.write("Running Setup Script...\n")
        # https://developers.google.com/appengine/articles/update_schema?hl=en

        # Swap the base class of <model> to db.Expando
        # Comment out required=True in HousingApplication.SemesterToBeginIndex
        # Comment out SemesterToBegin function in HousingApplication
        # Run this script
        # Swap the base clss back to db.model

        # 22 December 2012
        # update HousingApplication.SemesterToBegin to HousingApplication.SemesterToBeginIndex
        self.response.write("Updating SemesterToBegin to SemesterToBeginIndex...\n")
        from scripts.database_models.housingapplication import HousingApplication, get_index_from_semester_text
        q = HousingApplication.all()
        for app in q:
            self.response.write(app.FullName + "\n")
            if app.SemesterToBeginIndex:
                self.response.write("- Already updated\n")
            else:
                self.response.write("- Updating {}\n".format(app.SemesterToBegin))
                app.SemesterToBeginIndex = get_index_from_semester_text(app.SemesterToBegin)
                # do not delete until the old versions (Release 3 and lower) are no longer in use
                #del app.SemesterToBegin
                app.put()


application = webapp.WSGIApplication([
  ('/manage/setup', SetupHandler),
  ('/manage.*', ManageHandler),
  ], debug=BaseHandler.debug)
