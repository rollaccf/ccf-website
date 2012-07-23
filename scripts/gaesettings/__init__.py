"""Simple configurable settings module for GAE"""
from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

##  Name:(defaultValue, Catagory, DisplayName, Documentation, ReadOnlyBool)
DefaultValues = {
  'HomepageSlideRotationDelay':
  {
    'Value':4000,
    'Catagory':"homepage",
    'DisplayName':"Homepage Slide Rotation Delay",
    'Documentation':"Defines how long the delay is between switching slides\nTime is in milliseconds (1 second == 1000 milliseconds)",
    'ReadOnly':False,
  },
  'MaxHomepageSlides':
  {
    'Value':10,
    'Catagory':"homepage",
    'DisplayName':"Homepage Slide Max Enabled",
    'Documentation':"The max number of slides that can be enabled at one time",
    'ReadOnly':True,
  },
  'HousingApplicationCch_CompletionEmail':
  {
    'Value':"",
    'Catagory':"housing application",
    'DisplayName':"CCH Housing Application Completion Email",
    'Documentation':"This email is notified when a student completes the CCH Housing Application",
    'ReadOnly':False,
  },
  'HousingApplicationWcch_CompletionEmail':
  {
    'Value':"",
    'Catagory':"housing application",
    'DisplayName':"WCCH Housing Application Completion Email",
    'Documentation':"This email is notified when a student completes the WCCH Housing Application",
    'ReadOnly':False,
  },
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
        if isinstance(value['Value'], basestring):
          StringSetting(Name=key, **value).put()
        elif isinstance(value['Value'], int):
          IntSetting(Name=key, **value).put()
        elif isinstance(value['Value'], float):
          FloatSetting(Name=key, **value).put()
        else:
          raise GAESettingTypeNotSupported("type "+type(value['Value'])+" is not supported in gaesettings")

gaesettings = _gaesettings()
