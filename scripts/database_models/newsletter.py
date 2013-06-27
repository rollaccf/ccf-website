from google.appengine.ext import ndb, blobstore

from . import NdbBaseModel, NdbUtcDateTimeProperty


class Newsletter(NdbBaseModel):
    Createdby = ndb.UserProperty(auto_current_user_add=True)
    CreationDateTime = NdbUtcDateTimeProperty(auto_now_add=True)
    DisplayOrder = ndb.IntegerProperty()

    Title = ndb.StringProperty(
        verbose_name="Title",
        required=True,
    )
    NewsletterBlob = ndb.BlobKeyProperty(
        verbose_name="Newsletter",
        required=True,
    )
