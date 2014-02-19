from google.appengine.ext import ndb

from . import NdbBaseModel, NdbUtcDateTimeProperty, GaeFileField
from ext.wtforms import validators, fields
from ext.wtforms.form import Form


class StaffPosition_Form(Form):
    Name = fields.TextField(u'Name', validators=[validators.Required()])
    Image = GaeFileField(u'Image', validators=[validators.data_required()])
    Email = fields.TextField(u'Email', validators=[validators.Required()])
    Description = fields.TextAreaField(u'Description', validators=[validators.Required()])


class StaffPosition(NdbBaseModel):
    CreatedBy = ndb.UserProperty(auto_current_user_add=True)
    CreationDateTime = NdbUtcDateTimeProperty(auto_now_add=True)
    ModifiedBy = ndb.UserProperty(auto_current_user=True)
    ModifiedDateTime = NdbUtcDateTimeProperty(auto_now=True)
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
