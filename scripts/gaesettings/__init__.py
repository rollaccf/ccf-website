"""Simple configurable settings module for GAE"""
from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

class BaseSetting(polymodel.PolyModel):
  ReadOnly = ndb.BooleanProperty()
  Catagory = ndb.StringProperty()
  DisplayName = ndb.StringProperty() # I would use verbose_name instead, but I can't figure out how to use it
  Documentation = ndb.StringProperty()

class StringSetting(BaseSetting):
  Value = ndb.StringProperty()

class IntSetting(BaseSetting):
  Value = ndb.IntegerProperty()

class FloatSetting(BaseSetting):
  Value = ndb.FloatProperty()

class GAESettingDoesNotExist(Exception):
  pass

class GAESettingReadOnlyError(Exception):
  pass

class _gaesettings(object):
  def _getdbvalue(self, name):
    dbValue = BaseSetting.get_by_id(name)
    if dbValue == None:
      raise GAESettingDoesNotExist("'" +name + "' does not exist in the default values or in the datastore")
    return dbValue

  def __getattr__(self, name):
    dbValue = self._getdbvalue(name)
    return dbValue.Value

  def __setattr__(self, name, value):
    dbValue = self._getdbvalue(name)
    if dbValue.ReadOnly == True:
      raise GAESettingReadOnlyError("Can not set the value of '" +name + "' it is read only")
    dbValue.Value = value
    dbValue.put()

gaesettings = _gaesettings()
