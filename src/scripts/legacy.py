from google.appengine.ext import webapp
from scripts import BaseHandler
from scripts.database_models.rapi_image import RaPiImage

class Legacy_BaseHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(Legacy_BaseHandler, self).__init__(*args, **kwargs)


class LegacyHandler(Legacy_BaseHandler):
    def get(self):
        self.template_vars["latest_image"] = RaPiImage.query().order(-RaPiImage.DateTime).get()
        self.render_template("legacy/legacy.html")


class LegacyDonateHandler(Legacy_BaseHandler):
    def get(self):
        self.render_template("legacy/donate.html")

class LegacyTimeLapseHandler(Legacy_BaseHandler):
    def get(self):
        self.template_vars["latest_image"] = RaPiImage.query().order(-RaPiImage.DateTime).get()
        self.render_template("legacy/time_lapse.html")


application = webapp.WSGIApplication([
    ('/legacy/?', LegacyHandler),
    ('/legacy/donate.*', LegacyDonateHandler),
    ('/legacy/time_lapse', LegacyTimeLapseHandler),
    ], debug=BaseHandler.debug)
