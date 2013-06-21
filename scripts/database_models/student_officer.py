from . import NdbBaseModel, NdbUtcDateTimeProperty
from cgi import FieldStorage
from google.appengine.ext import ndb
from wtforms import validators
from wtforms.form import Form
from wtforms.fields import *


class StudentOfficer_Form(Form):
    Image = FileField(u'Image')
    Position = TextField(u'Officer Position', validators=[validators.Required()])
    Name = TextField(u'Officer Name', validators=[validators.Required()])
    Major = TextField(u'Officer Major', validators=[validators.Required()])
    Grade = TextField(u'Officer Grade', validators=[validators.Required()])
    Email = TextField(u'Officer Email', validators=[validators.Required()])

    def validate_Image(form, field):
        # validators.DateRequired or validators.InputRequired will not work
        # since a FieldStorage instance does not return true in an if statement
        if isinstance(field.data, FieldStorage):
            field.data = field.data.value
        elif hasattr(form, 'isEdit') and form.isEdit is True:
            pass
        else:
            raise validators.ValidationError("An Image is required."+ str(type(field.data)) )


class StudentOfficer(NdbBaseModel):
    Createdby = ndb.UserProperty(auto_current_user_add=True)
    CreationDateTime = NdbUtcDateTimeProperty(auto_now_add=True)
    DisplayOrder = ndb.IntegerProperty()

    Image = ndb.BlobProperty(
      required=True,
    )
    Position = ndb.StringProperty(
      required=True,
    )
    Name = ndb.StringProperty(
      required=True,
    )
    Major = ndb.StringProperty(
      required=True,
    )
    Grade = ndb.StringProperty(
      required=True,
    )
    Email = ndb.StringProperty(
      required=True,
    )