from google.appengine.ext import db, blobstore

from . import BaseModel, UtcDateTimeProperty


class Newsletter(BaseModel):
    Createdby = db.UserProperty(auto_current_user_add=True)
    CreationDateTime = UtcDateTimeProperty(auto_now_add=True)
    DisplayOrder = db.IntegerProperty()

    Title = db.StringProperty(
        verbose_name="Title",
        required=True,
    )
    NewsletterBlob = blobstore.BlobReferenceProperty(
        verbose_name="Newsletter",
        required=True,
    )
