from google.appengine.ext import webapp
from scripts import BaseHandler
from scripts.database_models.rapi_config import RaPiConfig
from scripts.database_models.rapi_image import RaPiImage, RaPiImage_Form


class Rapi_BaseHandler(BaseHandler):
    pass

class RapiSettings_Handler(Rapi_BaseHandler):
    def get(self, rapi_name):
        # TODO: save access time

        print(rapi_name)
        r = RaPiConfig.get_by_id(rapi_name)
        self.response.write(r.to_yaml())
        self.response.headers.add("Content-Type", "text/plain")


class RapiUpload_Handler(Rapi_BaseHandler):
    def post(self):
        self.process_form(RaPiImage_Form, RaPiImage, raise_on_error=True)


application = webapp.WSGIApplication([
    ('/rapi/upload', RapiUpload_Handler),
    ('/rapi/([^/]+)', RapiSettings_Handler),
    ], debug=BaseHandler.debug)
