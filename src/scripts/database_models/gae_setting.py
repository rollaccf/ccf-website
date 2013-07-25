"""Simple configurable settings module for GAE"""
from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel
from wtforms.form import Form
from wtforms.fields import TextField, TextAreaField, SelectField

class NewSetting_Form(Form):
    Name=TextField("Name")
    Value=TextField("Value")
    ValueType=SelectField('Value Type',
        choices=[
            ('float', 'Float'),
            ('int', 'Int'),
            ('unicode', 'String'),
        ],
    )
    Category=TextField("Category")
    Documentation=TextAreaField("Documentation")

class BaseSetting(polymodel.PolyModel):
    Category = ndb.StringProperty()
    Documentation = ndb.StringProperty()


class StringSetting(BaseSetting):
    Value = ndb.StringProperty()


class IntSetting(BaseSetting):
    Value = ndb.IntegerProperty()


class FloatSetting(BaseSetting):
    Value = ndb.FloatProperty()
