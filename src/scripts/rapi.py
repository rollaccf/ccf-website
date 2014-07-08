from google.appengine.ext import webapp
from scripts import BaseHandler
from scripts.database_models.rapi_config import RaPiConfig


class Rapi_BaseHandler(BaseHandler):
    pass

class RapiHandler(Rapi_BaseHandler):
    def get(self, rapi_name):
        # TODO: save access time

        print(rapi_name)
        r = RaPiConfig.get_by_id(rapi_name)
        self.response.write(r.to_yaml())
        self.response.headers.add("Content-Type", "text/plain")

application = webapp.WSGIApplication([
    ('/rapi/([^/]+)', RapiHandler),
    ], debug=BaseHandler.debug)
