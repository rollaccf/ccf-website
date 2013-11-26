from cgi import FieldStorage

from google.appengine.ext import ndb

from . import NdbBaseModel, NdbUtcDateTimeProperty
from ext.wtforms import validators, fields
from ext.wtforms.form import Form


class WeekInfo_Form(Form):
    Date = fields.TextField()
    Speaker = fields.TextField()
    Topic = fields.TextField()
    Location = fields.TextField()


class SemesterSeries_Form(Form):
    Image = fields.FileField(u'Image')
    Title = fields.TextField(u'Title', validators=[validators.Required()])
    Description = fields.TextAreaField(u'Description',
                                               validators=[validators.Required(), validators.length(max=500)])
    Weeks = fields.FieldList(fields.FormField(WeekInfo_Form))

    def validate_Image(self, field):
        # validators.DateRequired or validators.InputRequired will not work
        # since a FieldStorage instance does not return true in an if statement
        if isinstance(field.data, FieldStorage):
            field.data = field.data.value
        elif hasattr(self, 'isEdit') and self.isEdit is True:
            pass
        else:
            raise validators.ValidationError("An Image is required.")


class WeekInfo(NdbBaseModel):
    Date = ndb.StringProperty(
        required=True,
    )
    Speaker = ndb.StringProperty()
    Topic = ndb.StringProperty()
    Location = ndb.StringProperty()


class SemesterSeries(NdbBaseModel):
    Createdby = ndb.UserProperty(auto_current_user_add=True)
    CreationDateTime = NdbUtcDateTimeProperty(auto_now_add=True)

    Image = ndb.BlobProperty(
        required=True,
    )
    Title = ndb.StringProperty(
        required=True,
    )
    Description = ndb.TextProperty(
        required=True,
    )
    Weeks = ndb.LocalStructuredProperty(
        WeekInfo,
        repeated=True,
    )

