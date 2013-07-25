from cgi import FieldStorage

from google.appengine.ext import ndb

from . import NdbBaseModel, NdbUtcDateTimeProperty
from wtforms import validators, fields
from wtforms.form import Form


class StaffPosition_Form(Form):
    Name = fields.TextField(u'Name', validators=[validators.Required()])
    Image = fields.FileField(u'Image')
    Email = fields.TextField(u'Email', validators=[validators.Required()])
    Description = fields.TextAreaField(u'Description', validators=[validators.Required()])


    def validate_Image(self, field):
        # validators.DateRequired or validators.InputRequired will not work
        # since a FieldStorage instance does not return true in an if statement
        if isinstance(field.data, FieldStorage):
            field.data = field.data.value
        elif hasattr(self, 'isEdit') and self.isEdit is True:
            pass
        else:
            raise validators.ValidationError("An Image is required." + str(type(field.data)))


class StaffPosition(NdbBaseModel):
    CreatedBy = ndb.UserProperty(auto_current_user_add=True)
    CreationDateTime = NdbUtcDateTimeProperty(auto_now_add=True)
    DisplayOrder = ndb.IntegerProperty()

    Name = ndb.StringProperty(
        required=True,
    )
    Image = ndb.BlobProperty(
        required=True,
    )
    Email = ndb.StringProperty(
    )
    Description = ndb.TextProperty(
        required=True,
    )
