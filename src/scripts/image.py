import datetime
from google.appengine.ext import ndb
from google.appengine.ext import webapp
from scripts import BaseHandler


class Image(BaseHandler):
    def get(self, encoded_key):
        model = None
        try:
            model = ndb.Key(urlsafe=encoded_key).get()
        except:
            self.abort(404, "Image Does Not Exist")

        if model and model.Image:
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

