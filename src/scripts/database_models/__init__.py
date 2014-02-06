from cgi import FieldStorage

from google.appengine.ext import ndb
from scripts.utils.tzinfo import utc, Central

from ext.wtforms import fields


class NdbBaseModel(ndb.Model):
    def __getattr__(self, name):
        """
        easily get a datetime as central time
        ex name: CreationDateTime_cdt
        """
        ndb_utc_property_types = (NdbUtcDateTimeProperty, NdbUtcDateProperty, NdbUtcTimeProperty)
        try:
            prop, tz = name.split('_')
            if prop in self._properties and isinstance(self._properties[prop], ndb_utc_property_types):
                return getattr(self, prop).astimezone(Central)
            else:
                super(NdbBaseModel, self).__getattribute__(name)
        except Exception:
            super(NdbBaseModel, self).__getattribute__(name)


class NdbUtcDateTimeProperty(ndb.DateTimeProperty):
    """
    Marks DateTimeProperty values returned from the datastore as UTC. Ensures
    all values destined for the datastore are converted to UTC if marked with an
    alternate Timezone.

    Inspired by
    http://www.letsyouandhimfight.com/2008/04/12/time-zones-in-google-app-engine/
    http://code.google.com/appengine/articles/extending_models.html
    """

    def _to_base_type(self, value):
        """
        Returns the value for writing to the datastore. If value has a tzinfo,
        convert it to UTC then remove the timezone info so that gae with accept it.
        If tzinfo is not present we do not need to make changes.
        """
        if value.tzinfo:
            return value.astimezone(utc).replace(tzinfo=None)

    def _from_base_type(self, value):
        """
        Returns the value retrieved from the datastore. Ensures all dates
        are properly marked as UTC if not None
        """
        return value.replace(tzinfo=utc)


class NdbUtcDateProperty(ndb.DateProperty):
    """
    See class NdbUtcDateTimeProperty

    Dates do not have tzinfo
    """


class NdbUtcTimeProperty(ndb.TimeProperty):
    """
    See class NdbUtcDateTimeProperty
    """
    def _to_base_type(self, value):
        if value.tzinfo:
            return value.astimezone(utc).replace(tzinfo=None)

    def _from_base_type(self, value):
        return value.replace(tzinfo=utc)


class GaeFileField(fields.FileField):
    def process_formdata(self, valuelist):
        if len(valuelist) > 0:
            form_value = valuelist[0]
            if isinstance(form_value, FieldStorage):
                self.data = form_value.value
