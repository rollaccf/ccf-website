from google.appengine.ext import ndb

from . import NdbBaseModel, NdbUtcDateTimeProperty, GaeFileField
from ext.wtforms import validators, fields
from ext.wtforms.form import Form


class StudentOfficer_Form(Form):
    Image = GaeFileField(u'Image', validators=[validators.data_required()])
    Position = fields.TextField(u'Officer Position', validators=[validators.Required()])
    Name = fields.TextField(u'Officer Name', validators=[validators.Required()])
    Major = fields.TextField(u'Officer Major', validators=[validators.Required()])
    Grade = fields.TextField(u'Officer Grade', validators=[validators.Required()])
    Email = fields.TextField(u'Officer Email', validators=[validators.Required()])


class StudentOfficer(NdbBaseModel):
    relevant_page_urls = ["/aboutus/staff"]

    Createdby = ndb.UserProperty(auto_current_user_add=True)
    CreationDateTime = NdbUtcDateTimeProperty(auto_now_add=True)
    ModifiedBy = ndb.UserProperty(auto_current_user=True)
    ModifiedDateTime = NdbUtcDateTimeProperty(auto_now=True)
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
