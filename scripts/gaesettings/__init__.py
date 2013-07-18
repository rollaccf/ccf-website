"""Simple configurable settings module for GAE"""
from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel


class BaseSetting(polymodel.PolyModel):
    Category = ndb.StringProperty()
    Documentation = ndb.StringProperty()


class StringSetting(BaseSetting):
    Value = ndb.StringProperty()


class IntSetting(BaseSetting):
    Value = ndb.IntegerProperty()


class FloatSetting(BaseSetting):
    Value = ndb.FloatProperty()


class GAESettingDoesNotExist(Exception):
    pass


class _gaesettings(object):
    def _getdbvalue(self, name):
        dbValue = BaseSetting.get_by_id(name)
        if dbValue == None:
            raise GAESettingDoesNotExist("'" + name + "' does not exist in the default values or in the datastore")
        return dbValue

    def __getattr__(self, name):
        dbValue = self._getdbvalue(name)
        return dbValue.Value

    def __setattr__(self, name, value):
        dbValue = self._getdbvalue(name)
        dbValue.Value = value
        dbValue.put()


gaesettings = _gaesettings()
