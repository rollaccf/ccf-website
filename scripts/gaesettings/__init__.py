"""Simple configurable settings module for GAE"""
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext.db import polymodel, GqlQuery

##  Name:(defaultValue, Catagory, DisplayName, Documentation, ReadOnlyBool)
DefaultValues = {
  'HomepageSlideRotationDelay':(4000, "homepage",
    "Homepage Slide Rotation Delay",
    "Defines how long the delay is between switching slides\nTime is in milliseconds (1 second == 1000 milliseconds)",
    False),
  'HomepageLinkPrefix':("slide", "homepage",
    "Homepage Slide Link Prefix",
    "The prefix of the URL for the homepage Slides",
    True),
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
  ReadOnly = db.BooleanProperty()
  Name = db.StringProperty()
  Catagory = db.CategoryProperty()
  DisplayName = db.StringProperty() # I would use verbose_name instead, but I can't figure out how to use it
  Documentation = db.StringProperty(multiline=True)

class StringSetting(BaseSetting):
  Value = db.StringProperty()

class IntSetting(BaseSetting):
  Value = db.IntegerProperty()

class FloatSetting(BaseSetting):
  Value = db.FloatProperty()

class GAESettingDoesNotExist(BaseException):
  pass

class GAESettingTypeNotSupported(BaseException):
  pass

class GAESettingReadOnlyError(BaseException):
  pass

class _gaesettings(object):
  def __getattr__(self, name):
    value = memcache.get("gaesettings_"+name)
    if value == None:
      dbValue = GqlQuery("SELECT * FROM BaseSetting WHERE Name = :1", name).get();
      if dbValue == None:
        self.CreateNonexistantValuesInDataStore()
        dbValue = GqlQuery("SELECT * FROM BaseSetting WHERE Name = :1", name).get();
        if dbValue == None:
          raise GAESettingDoesNotExist("'" +name + "' does not exist in the default values or in the datastore")
      memcache.set("gaesettings_"+name, dbValue.Value)
      return dbValue.Value
    else:
      return value

  def __setattr__(self, name, value):
    dbValue = GqlQuery("SELECT * FROM BaseSetting WHERE Name = :1", name).get();
    if dbValue == None:
      self.CreateNonexistantValuesInDataStore()
      dbValue = GqlQuery("SELECT * FROM BaseSetting WHERE Name = :1", name).get();
      if dbValue == None:
        raise GAESettingDoesNotExist("'" +name + "' does not exist in the datastore")
    if dbValue.ReadOnly == True:
      raise GAESettingReadOnlyError("Can not set the value of '" +name + "' it is read only")
    dbValue.Value = value
    dbValue.put()
    memcache.set("gaesettings_"+name, dbValue.Value)

  def CreateNonexistantValuesInDataStore(self):
    q = GqlQuery("SELECT * FROM BaseSetting WHERE Name = :1")
    for key,value in DefaultValues.items():
      q.bind(key)
      dbValue = q.get()
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
