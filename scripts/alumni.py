import urllib
from google.appengine.ext import webapp, blobstore
from google.appengine.ext.webapp import blobstore_handlers
from scripts import BaseHandler
from scripts.database_models.newsletter import Newsletter

class Alumni_BaseHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
      BaseHandler.__init__(self, *args, **kwargs)
      self.template_vars = {
        'AlumniSelected':"top-level-dropdown-selected",
      }

class MinistryHappeningsHandler(Alumni_BaseHandler):
    def get(self):
        self.render_template("alumni/ministry_happenings.html", self.template_vars)

class PastEventsHandler(Alumni_BaseHandler):
    def get(self):
        self.render_template("alumni/past_events.html", self.template_vars)

class DonateHandler(Alumni_BaseHandler):
    def get(self):
        self.render_template("alumni/donate.html", self.template_vars)

class NewsletterHandler(Alumni_BaseHandler):
    def get(self):
        self.template_vars['Newsletters'] = Newsletter.gql("ORDER BY DisplayOrder DESC").fetch(50)
        self.render_template("alumni/newsletter.html", self.template_vars)

class NewsletterArchiveServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)


application = webapp.WSGIApplication([
  ('/alumni/newsletter/?', NewsletterHandler),
  ('/alumni/newsletter/([^/]+)', NewsletterArchiveServeHandler),
  ('/alumni/ministry_happenings.*', MinistryHappeningsHandler),
  ('/alumni/past_events.*', PastEventsHandler),
  ('/alumni/donate.*', DonateHandler),
  ], debug=BaseHandler.debug)
