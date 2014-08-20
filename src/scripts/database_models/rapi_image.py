from google.appengine.ext import ndb

from . import NdbBaseModel, NdbUtcDateTimeProperty, GaeFileField
from ext.wtforms import validators, fields
from ext.wtforms.form import Form


class RaPiImage_Form(Form):
    RapiId = fields.TextField(validators=[validators.data_required()])
    DateTime = fields.DateTimeField(validators=[validators.data_required()])
    Image = GaeFileField(validators=[validators.data_required()])


class RaPiImage(NdbBaseModel):
    RapiId = ndb.StringProperty()
    DateTime = NdbUtcDateTimeProperty()
    Image = ndb.BlobProperty()

