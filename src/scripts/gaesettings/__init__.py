"""Simple configurable settings module for GAE"""
from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

def CreateNonexistantValuesInDataStore():
  """Loads the default models into the datastore"""
  IntSetting.get_or_insert(
    'HomepageSlideRotationDelay',
    Value=4000,
    Catagory="homepage",
    DisplayName="Homepage Slide Rotation Delay",
    Documentation="Defines how long the delay is between switching slides\nTime is in milliseconds (1 second == 1000 milliseconds)",
    ReadOnly=False,
  )
  IntSetting.get_or_insert(
    'MaxHomepageSlides',
    Value=10,
    Catagory="homepage",
    DisplayName="Homepage Slide Max Enabled",
    Documentation="The max number of slides that can be enabled at one time",
    ReadOnly=True,
  )
  StringSetting.get_or_insert(
    'HousingApplicationCch_CompletionEmail',
    Value="",
    Catagory="housing application",
    DisplayName="CCH Housing Application Completion Email",
    Documentation="This email is notified when a student completes the CCH Housing Application",
    ReadOnly=False,
  )
  StringSetting.get_or_insert(
    'HousingApplicationWcch_CompletionEmail',
    Value="",
    Catagory="housing application",
    DisplayName="WCCH Housing Application Completion Email",
    Documentation="This email is notified when a student completes the WCCH Housing Application",
    ReadOnly=False,
  )
  IntSetting.get_or_insert(
    'HousingApplication_ReminderEmailDelayDays',
    Value=7,
    Catagory="housing application",
    DisplayName="Housing Application Reminder Email Delay",
    Documentation="The number of days to wait before sending a reminder email for unprocessed housing applications",
    ReadOnly=False,
  )
  StringSetting.get_or_insert(
    'google_checkout_sandbox_merchant_id',
    Value="221363761688324",
    Catagory="google checkout",
    DisplayName="Google Checkout Sandbox Merchant ID",
    Documentation="Google Checkout Sandbox Merchant ID",
    ReadOnly=True,
  )
  StringSetting.get_or_insert(
    'google_checkout_sandbox_merchant_key',
    Value="bnuortYYfllYz30Rv00ETg",
    Catagory="google checkout",
    DisplayName="Google Checkout Sandbox Merchant Key",
    Documentation="Google Checkout Sandbox Merchant Key",
    ReadOnly=True,
  )
  StringSetting.get_or_insert(
    'google_checkout_merchant_id',
    Value="",
    Catagory="google checkout",
    DisplayName="Google Checkout Merchant ID",
    Documentation="Google Checkout Merchant ID",
    ReadOnly=True,
  )
  StringSetting.get_or_insert(
    'google_checkout_merchant_key',
    Value="",
    Catagory="google checkout",
    DisplayName="Google Checkout Merchant Key",
    Documentation="Google Checkout Merchant Key",
    ReadOnly=True,
  )
  BoolSetting.get_or_insert(
    'google_checkout_use_sandbox',
    Value=True,
    Catagory="google checkout",
    DisplayName="Google Checkout Enable Sandbox",
    Documentation="Google Checkout Enable Sandbox",
    ReadOnly=True,
  )


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

class BoolSetting(BaseSetting):
  Value = ndb.BooleanProperty()

class GAESettingDoesNotExist(Exception):
  pass

class GAESettingReadOnlyError(Exception):
  pass

class _gaesettings(object):
  def _getdbvalue(self, name):
    dbValue = BaseSetting.get_by_id(name)
    if dbValue == None:
      CreateNonexistantValuesInDataStore()
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
