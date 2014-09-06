import datetime
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
    def __init__(self, *args, **kwargs):
        super(LegacyTimeLapseHandler, self).__init__(*args, **kwargs)
        self.use_cache = False

    def get(self, date_time):
        if date_time:
            try:
                date = datetime.datetime.strptime(date_time, "/%Y-%m-%d %H:%M:%S")
                image = RaPiImage.query().filter(RaPiImage.DateTime == date).get()
                if not image:
                    raise ValueError
                self.template_vars["current_image"] = image
            except ValueError:
                self.redirect('/legacy/time_lapse')
                return
        else:
            self.template_vars["current_image"] = RaPiImage.query().order(-RaPiImage.DateTime).get()
            date = self.template_vars["current_image"].DateTime

        self.template_vars["before_image"] = RaPiImage.query().filter(RaPiImage.DateTime < date).order(-RaPiImage.DateTime).get()
        self.template_vars["after_image"] = RaPiImage.query().filter(RaPiImage.DateTime > date).order(RaPiImage.DateTime).get()
        self.render_template("legacy/time_lapse.html")


application = webapp.WSGIApplication([
    ('/legacy/?', LegacyHandler),
    ('/legacy/donate.*', LegacyDonateHandler),
    ('/legacy/time_lapse(/[^/]+)?', LegacyTimeLapseHandler),
    ], debug=BaseHandler.debug)
