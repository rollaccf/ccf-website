from google.appengine.ext import db, ndb
from scripts.utils.tzinfo import utc, Central


class BaseModel(db.Model):
    def Update(self, data):
        """Updates each field in the model with the corresponding value in the UnicodeMultiDict data"""
        properties = self.properties()
        for prop in properties:
            if prop in data and data[prop] != None:
                if type(properties[prop]).__name__ == "BlobProperty":
                    if hasattr(data[prop], 'value'):
                        setattr(self, prop, db.Blob(data[prop].value))
                else:
                    setattr(self, prop, data[prop])

    def PrintEscapedParagraph(self, mode_property):
        from cgi import escape
        # This is probably a bad way to do this, but I cannot think of any other
        return escape(getattr(self, mode_property)).replace('\n', '<br />')

    def __getattr__(self, name):
        """easily get a datetime as central time
           ex name: CreationDateTime_cdt
        """
        try:
            prop, tz = name.split('_')
            if prop in self.properties() and isinstance(self.properties()[prop], UtcDateTimeProperty) and tz == "cdt":
                return getattr(self, prop).astimezone(Central)
            else:
                raise AttributeError
        except:
            raise AttributeError


class UtcDateTimeProperty(db.DateTimeProperty):
    """Marks DateTimeProperty values returned from the datastore as UTC. Ensures
    all values destined for the datastore are converted to UTC if marked with an
    alternate Timezone.

    Inspired by
    http://www.letsyouandhimfight.com/2008/04/12/time-zones-in-google-app-engine/
    http://code.google.com/appengine/articles/extending_models.html
    """

    def get_value_for_datastore(self, model_instance):
        """Returns the value for writing to the datastore. If value is None,
        return None, else ensure date is converted to UTC. Note Google App
        Engine already does this. Called by datastore
        """
        date = super(UtcDateTimeProperty, self).get_value_for_datastore(model_instance)
        if date:
            if date.tzinfo:
                return date.astimezone(utc)
            else:
                return date.replace(tzinfo=utc)
        else:
            return None

    def make_value_from_datastore(self, value):
        """Returns the value retrieved from the datastore. Ensures all dates
        are properly marked as UTC if not None"""
        if value is None:
            return None
        else:
            return value.replace(tzinfo=utc)


class NdbBaseModel(ndb.Model):
    def __getattr__(self, name):
        """easily get a datetime as central time
           ex name: CreationDateTime_cdt
        """
        try:
            prop, tz = name.split('_')
            if prop in self.properties() and isinstance(self.properties()[prop], UtcDateTimeProperty):
                return getattr(self, prop).astimezone(Central)
            else:
                raise AttributeError
        except:
            raise AttributeError


class NdbUtcDateTimeProperty(ndb.DateTimeProperty):
    """Marks DateTimeProperty values returned from the datastore as UTC. Ensures
    all values destined for the datastore are converted to UTC if marked with an
    alternate Timezone.

    Inspired by
    http://www.letsyouandhimfight.com/2008/04/12/time-zones-in-google-app-engine/
    http://code.google.com/appengine/articles/extending_models.html
    """

    def get_value_for_datastore(self, model_instance):
        """Returns the value for writing to the datastore. If value is None,
        return None, else ensure date is converted to UTC. Note Google App
        Engine already does this. Called by datastore
        """
        # TODO: fix this call. We are in NdbUtcDateTimeProperty not UtcDateTimeProperty
        date = super(UtcDateTimeProperty, self).get_value_for_datastore(model_instance)
        if date:
            if date.tzinfo:
                return date.astimezone(utc)
            else:
                return date.replace(tzinfo=utc)
        else:
            return None

    def make_value_from_datastore(self, value):
        """Returns the value retrieved from the datastore. Ensures all dates
        are properly marked as UTC if not None"""
        if value is None:
            return None
        else:
            return value.replace(tzinfo=utc)
