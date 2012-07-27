from google.appengine.ext import db, blobstore

class BaseModel(db.Model):

  def Update(self, data):
    """Updates each field in the model with the corresponding value in the UnicodeMultiDict data"""
    properties = self.properties()
    for prop in properties:
      if prop in data and data[prop] != None:
        if type(properties[prop]).__name__ == "BlobProperty":
          setattr(self, prop, db.Blob(data[prop].value))
        else:
          setattr(self, prop, data[prop])

  def PrintEscapedParagraph(self, property):
    from cgi import escape
    """This is probably a bad way to do this, but I cannot think of any other"""
    return escape(getattr(self, property)).replace('\n', '<br />')
