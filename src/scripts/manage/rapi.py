import yaml
from google.appengine.api import images
from google.appengine.ext import webapp, ndb
from . import Manage_BaseHandler
from scripts.database_models.rapi_config import RaPiConfig, RaPiConfig_Form


class Manage_RaPi_BaseHandler(Manage_BaseHandler):
    pass


class Manage_RaPi_Handler(Manage_RaPi_BaseHandler):
    def get(self):
        # list RaPis with last checkin time and edit ability
        #r = RaPiConfig(id="test", Interval=600, UploadLocation="asdf")
        #r.put()
        #self.response.out.write("Wrote it!")
        r = RaPiConfig.get_by_id("test")
        d = r.to_dict()
        del d['CreatedBy']
        del d['CreationDateTime']
        del d['ModifiedDateTime']
        del d['ModifiedBy']
        for k, v in d.items():
            if isinstance(v, unicode):
                d[k] = str(v)
        self.response.write(yaml.dump(d,  default_flow_style=False))
        self.response.headers.add("Content-Type", "text/plain")
        pass


class Manage_RaPi_EditHandler(Manage_RaPi_BaseHandler):
    def get(self, rapi_name):
        # list RaPi settings
        pass

    def post(self):
        # save settings
        pass


application = webapp.WSGIApplication([
    ('/manage/rapi/edit/([^/]+)', Manage_RaPi_EditHandler),
    ('/manage/rapi.*', Manage_RaPi_Handler),
    ], debug=Manage_BaseHandler.debug)
