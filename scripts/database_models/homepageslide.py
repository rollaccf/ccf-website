from . import BaseModel, UtcDateTimeProperty
from google.appengine.ext import db

class HomepageSlide(BaseModel):
  Enabled = db.BooleanProperty()
  DisplayOrder = db.IntegerProperty()

  Createdby = db.UserProperty(auto_current_user_add=True)
  CreationDateTime = UtcDateTimeProperty(auto_now_add=True)
  Modifiedby = db.UserProperty(auto_current_user=True)
  ModifiedDateTime = UtcDateTimeProperty(auto_now=True)

  Image = db.BlobProperty(
    verbose_name="Carousel Image",
  )
  Link = db.StringProperty(
    verbose_name="URL",
  )
  Title = db.StringProperty(
    verbose_name="Page Title",
  )
  Html = db.TextProperty(
    verbose_name="Page Content",
  )

  @db.ComputedProperty
  def CompleteURL(self):
    return '/' + self.Link
