from google.appengine.ext import webapp
from scripts.main import BaseHandler


class Manage_BaseHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(Manage_BaseHandler, self).__init__(*args, **kwargs)
        self.use_cache = False


class ManageHandler(Manage_BaseHandler):
    def get(self):
        self.render_template("manage/manage.html")


class SetupHandler(Manage_BaseHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/plain"
        self.response.write("Running Setup Script...\n")
        # https://developers.google.com/appengine/articles/update_schema?hl=en

        # TODO: auto convert model base class to Expando
        # http://stackoverflow.com/questions/9539052/python-dynamically-changing-base-classes-at-runtime-how-to
        # Swap the base class of <model> to db.Expando
        # Comment out required=True in HousingApplication.SemesterToBeginIndex
        # Comment out SemesterToBegin function in HousingApplication
        # Run this script
        # Swap the base class back to db.model

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


class TestHandler(Manage_BaseHandler):
    def get(self, action):
        if action == "500":
            self.abort(500)
        elif action == "404":
            self.abort(404)
        elif action == "exception":
            raise Exception("Test Exception")


application = webapp.WSGIApplication([
    ('/manage/_test/([^/]+)', TestHandler),
    ('/manage/_setup', SetupHandler),
    ('/manage.*', ManageHandler),
    ], debug=Manage_BaseHandler.debug)
