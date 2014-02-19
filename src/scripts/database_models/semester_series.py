from google.appengine.ext import ndb

from . import NdbBaseModel, NdbUtcDateTimeProperty, GaeFileField
from ext.wtforms import validators, fields
from ext.wtforms.form import Form


class WeekInfo_Form(Form):
    Date = fields.TextField()
    Speaker = fields.TextField()
    Topic = fields.TextField()
    Location = fields.TextField()


class SemesterSeries_Form(Form):
    Image = GaeFileField(u'Image', validators=[validators.data_required()])
    Title = fields.TextField(u'Title', validators=[validators.Required()])
    Description = fields.TextAreaField(u'Description', validators=[validators.Required(), validators.length(max=500)])
    Weeks = fields.FieldList(fields.FormField(WeekInfo_Form))


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
    ModifiedBy = ndb.UserProperty(auto_current_user=True)
    ModifiedDateTime = NdbUtcDateTimeProperty(auto_now=True)

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

