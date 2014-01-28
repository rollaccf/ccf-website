import datetime
from google.appengine.ext import ndb
from google.appengine.ext import webapp
from scripts import BaseHandler
# import all the types that have images
from database_models.homepageslide import HomepageSlide
from database_models.semester_series import SemesterSeries
from database_models.staff_position import StaffPosition
from database_models.student_officer import StudentOfficer


class Image(BaseHandler):
    def head(self):
        two_days_in_seconds = 172800
        expires_date = datetime.datetime.now() + datetime.timedelta(days=2)
        HTTP_HEADER_FORMAT = "%a, %d %b %Y %H:%M:00 GMT"

        self.response.headers['Expires'] = expires_date.strftime(HTTP_HEADER_FORMAT)
        self.response.headers['Cache-Control'] = "public, max-age=%s" % two_days_in_seconds
        self.response.headers['Content-Type'] = "image/png"

    def get(self, encoded_key):
        model = ndb.Key(urlsafe=encoded_key).get()

        if model and hasattr(model, "Image") and model.Image:
            two_days_in_seconds = 172800
            expires_date = datetime.datetime.now() + datetime.timedelta(days=2)
            HTTP_HEADER_FORMAT = "%a, %d %b %Y %H:%M:00 GMT"

            self.response.headers['Expires'] = expires_date.strftime(HTTP_HEADER_FORMAT)
            self.response.headers['Cache-Control'] = "public, max-age=%s" % two_days_in_seconds
            self.response.headers['Content-Type'] = "image/png"
            self.response.out.write(model.Image)
        else:
            self.abort(404, "Image Does Not Exist")


application = webapp.WSGIApplication([
    ('/image/([^/]+)', Image),
    ], debug=BaseHandler.debug)

