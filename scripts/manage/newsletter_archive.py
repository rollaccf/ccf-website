import urllib
from google.appengine.ext import webapp, blobstore
from google.appengine.ext.webapp import blobstore_handlers
from scripts.main import BaseHandler
from scripts.database_models.newsletter import Newsletter

class ManageNewsletterArchiveHandler(BaseHandler):
    def get(self):
      self.render_template("manage/newsletter_archive/newsletter_archive.html",
      { 'title':"Manage Newsletter Archive",
        'uploadURL':blobstore.create_upload_url('/manage/newsletter_archive/upload'),
        'Newsletters':Newsletter.gql("ORDER BY DisplayOrder DESC").fetch(50),
      },use_cache=False)

class ManageNewsletterArchiveUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
  def post(self):
    newNewsletter = Newsletter(
      Title=self.request.get("title"),
      NewsletterBlob=self.get_uploads('file')[0],
    )
    displayOrderObject = Newsletter.gql("ORDER BY DisplayOrder DESC").get()
    newNewsletter.DisplayOrder = displayOrderObject.DisplayOrder + 1 if displayOrderObject else 1
    newNewsletter.put()
    self.redirect('/manage/newsletter_archive')

class ManageNewsletterArchiveServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, resource):
    resource = str(urllib.unquote(resource))
    blob_info = blobstore.BlobInfo.get(resource)
    self.send_blob(blob_info)

class ManageNewsletterArchiveDeleteHandler(BaseHandler):
  def get(self, resource):
    resource = str(urllib.unquote(resource))
    newsletter = Newsletter.get(resource)
    newsletter.NewsletterBlob.delete()
    newsletter.delete()
    self.redirect('/manage/newsletter_archive')

class ManageNewsletterArchiveOrderHandler(BaseHandler):
  def get(self, direction, displayOrderToMove):
    displayOrderToMove = int(displayOrderToMove)
    # I am assuming displayOrder has no duplicates
    FirstObject = Newsletter.gql("WHERE DisplayOrder = :1", displayOrderToMove).get()
    if direction == 'u':
      SecondObject = Newsletter.gql("WHERE DisplayOrder > :1 ORDER BY DisplayOrder ASC", displayOrderToMove).get()
    else:
      SecondObject = Newsletter.gql("WHERE DisplayOrder < :1 ORDER BY DisplayOrder DESC", displayOrderToMove).get()
    FirstObject.DisplayOrder, SecondObject.DisplayOrder = SecondObject.DisplayOrder, FirstObject.DisplayOrder
    FirstObject.put()
    SecondObject.put()
    self.redirect('/manage/newsletter_archive')


application = webapp.WSGIApplication([
  ('/manage/newsletter_archive/order/([ud])/(\d+)', ManageNewsletterArchiveOrderHandler),
  ('/manage/newsletter_archive/delete/([^/]+)', ManageNewsletterArchiveDeleteHandler),
  ('/manage/newsletter_archive/serve/([^/]+)', ManageNewsletterArchiveServeHandler),
  ('/manage/newsletter_archive/upload.*', ManageNewsletterArchiveUploadHandler),
  ('/manage/newsletter_archive.*', ManageNewsletterArchiveHandler),
  ], debug=BaseHandler.debug)
