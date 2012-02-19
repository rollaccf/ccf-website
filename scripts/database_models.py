from google.appengine.ext import db

class HomepageSlide(db.Model):
  Enabled = db.BooleanProperty(required=True)

  Createdby = db.UserProperty(auto_current_user_add=True)
  CreationDateTime = db.DateTimeProperty(auto_now_add=True)
  Modifiedby = db.UserProperty(auto_current_user=True)
  ModifiedDateTime = db.DateTimeProperty(auto_now=True)

  Image = db.BlobProperty(required=True)
  Link = db.LinkProperty(required=True)
  Title = db.StringProperty(required=True)
  Html = db.TextProperty(required=True)
  #TODO: add order property
