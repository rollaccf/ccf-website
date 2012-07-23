"""Simple configurable settings module for GAE"""
from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

##  Name:(defaultValue, Catagory, DisplayName, Documentation, ReadOnlyBool)
DefaultValues = {
  'HomepageSlideRotationDelay':(4000, "homepage",
    "Homepage Slide Rotation Delay",
    "Defines how long the delay is between switching slides\nTime is in milliseconds (1 second == 1000 milliseconds)",
    False),
  'MaxHomepageSlides':(10, "homepage",
    "Homepage Slide Max Enabled",
    "The max number of slides that can be enabled at one time",
    True),
  'HousingApplicationCch_CompletionEmail':
  (
    "",
    "housing application",
    "CCH Housing Application Completion Email",
    "This email is notified when a student completes the CCH Housing Application",
    False,
  ),
  'HousingApplicationWcch_CompletionEmail':
  (
    "",
    "housing application",
    "WCCH Housing Application Completion Email",
    "This email is notified when a student completes the WCCH Housing Application",
    False,
  ),
}

class BaseSetting(polymodel.PolyModel):
  ReadOnly = ndb.BooleanProperty()
  Name = ndb.StringProperty()
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

class GAESettingTypeNotSupported(Exception):
  pass

class GAESettingReadOnlyError(Exception):
  pass

class _gaesettings(object):
  def __getattr__(self, name):
    dbValue = ndb.gql("SELECT * FROM BaseSetting WHERE Name = :1", name).get();
    if dbValue == None:
      self.CreateNonexistantValuesInDataStore()
      dbValue = ndb.gql("SELECT * FROM BaseSetting WHERE Name = :1", name).get();
      if dbValue == None:
        raise GAESettingDoesNotExist("'" +name + "' does not exist in the default values or in the datastore")
    return dbValue.Value

  def __setattr__(self, name, value):
    dbValue = self.__getattr__(name)
    if dbValue.ReadOnly == True:
      raise GAESettingReadOnlyError("Can not set the value of '" +name + "' it is read only")
    dbValue.Value = value
    dbValue.put()

  def CreateNonexistantValuesInDataStore(self):
    unbound_query = ndb.gql("SELECT * FROM BaseSetting WHERE Name = :1")
    for key,value in DefaultValues.items():
      dbValue = unbound_query.bind(key).get()
      if dbValue == None:
        if isinstance(value[0], basestring):
          StringSetting(Name=key, Value=value[0], Catagory=value[1], DisplayName=value[2], Documentation=value[3], ReadOnly=value[4]).put()
        elif isinstance(value[0], int):
          IntSetting(Name=key, Value=value[0], Catagory=value[1], DisplayName=value[2], Documentation=value[3], ReadOnly=value[4]).put()
        elif isinstance(value[0], float):
          FloatSetting(Name=key, Value=value[0], Catagory=value[1], DisplayName=value[2], Documentation=value[3], ReadOnly=value[4]).put()
        else:
          raise GAESettingTypeNotSupported("type "+type(value[0])+" is not supported in gaesettings")

gaesettings = _gaesettings()
