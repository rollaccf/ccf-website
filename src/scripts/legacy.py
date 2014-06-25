from google.appengine.ext import webapp
from scripts import BaseHandler


class Legacy_BaseHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(Legacy_BaseHandler, self).__init__(*args, **kwargs)


class LegacyHandler(Legacy_BaseHandler):
    def get(self):
        self.render_template("legacy/legacy.html")


class LegacyDonateHandler(Legacy_BaseHandler):
    def get(self):
        self.render_template("legacy/donate.html")


application = webapp.WSGIApplication([
    ('/legacy/?', LegacyHandler),
    ('/legacy/donate.*', LegacyDonateHandler),
    ], debug=BaseHandler.debug)
