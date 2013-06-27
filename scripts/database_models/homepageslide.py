from cgi import FieldStorage

from google.appengine.ext import ndb

from . import NdbBaseModel, NdbUtcDateTimeProperty
from wtforms import validators, fields
from wtforms.form import Form


class HomepageSlide_Form(Form):
    Enabled = fields.BooleanField(u'Enabled')
    onHomepage = fields.BooleanField(u'onHomepage')

    Image = fields.FileField(u'Carousel Image')
    Link = fields.TextField(u'URL')
    Title = fields.TextField(u'Page Title')
    Html = fields.TextAreaField(u'Page Content')

    def validate_Image(self, field):
        # validators.DateRequired or validators.InputRequired will not work
        # since a FieldStorage instance does not return true in an if statement
        if isinstance(field.data, FieldStorage):
            field.data = field.data.value
        elif hasattr(self, 'isEdit') and self.isEdit is True:
            pass
        else:
            raise validators.ValidationError("An Image is required." + str(type(field.data)))


class HomepageSlide(NdbBaseModel):
    Enabled = ndb.BooleanProperty()
    DisplayOrder = ndb.IntegerProperty()

    Createdby = ndb.UserProperty(auto_current_user_add=True)
    CreationDateTime = NdbUtcDateTimeProperty(auto_now_add=True)
    Modifiedby = ndb.UserProperty(auto_current_user=True)
    ModifiedDateTime = NdbUtcDateTimeProperty(auto_now=True)

    Image = ndb.BlobProperty(
        verbose_name="Carousel Image",
    )
    Link = ndb.StringProperty(
        verbose_name="URL",
    )
    Title = ndb.StringProperty(
        verbose_name="Page Title",
    )
    Html = ndb.TextProperty(
        verbose_name="Page Content",
    )


    @ndb.ComputedProperty
    def onHomepage(self):
        return self.DisplayOrder is not None


    @ndb.ComputedProperty
    def CompleteURL(self):
        return '/' + self.Link
