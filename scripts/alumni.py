import urllib
from google.appengine.ext import webapp, blobstore
from google.appengine.ext.webapp import blobstore_handlers
from scripts.main import BaseHandler
from scripts.database_models import Newsletter

class MinistryHappeningsHandler(BaseHandler):
    def get(self):
        self.render_template("alumni/ministry_happenings.html",
        { 'title':"CCF Alumni",
          'AlumniSelected':"top-level-dropdown-selected",
          'Newsletters':Newsletter.gql("ORDER BY DisplayOrder DESC").fetch(50),
        })

class PastEventsHandler(BaseHandler):
    def get(self):
        self.render_template("alumni/past_events.html",
        { 'title':"CCF Alumni",
          'AlumniSelected':"top-level-dropdown-selected",
        })

class DonateHandler(BaseHandler):
    def get(self):
        self.render_template("alumni/donate.html",
        { 'title':"CCF Alumni",
          'AlumniSelected':"top-level-dropdown-selected",
        })

class NewsletterArchiveServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, resource):
    resource = str(urllib.unquote(resource))
    blob_info = blobstore.BlobInfo.get(resource)
    self.send_blob(blob_info)


application = webapp.WSGIApplication([
  ('/alumni/newsletter/([^/]+)', NewsletterArchiveServeHandler),
  ('/alumni/ministry_happenings.*', MinistryHappeningsHandler),
  ('/alumni/past_events.*', PastEventsHandler),
  ('/alumni/donate.*', DonateHandler),
  ], debug=True)
