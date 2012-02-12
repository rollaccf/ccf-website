from google.appengine.ext import db

class HomepageSlide(db.Model):
  Enabled = db.BooleanProperty()

  Createdby = db.UserProperty(auto_current_user_add=True)
  CreationDateTime = db.DateTimeProperty(auto_now_add=True)
  Modifiedby = db.UserProperty(auto_current_user=True)
  ModifiedDateTime = db.DateTimeProperty(auto_now=True)

  Image = db.BlobProperty()
  Link = db.LinkProperty()
  Html = db.TextProperty()
  #TODO: add order property
