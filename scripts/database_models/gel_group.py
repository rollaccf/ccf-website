import datetime
from . import BaseModel, UtcDateTimeProperty
from google.appengine.ext import db
from wtforms import validators
from wtforms.form import Form
from wtforms.fields import *


class DayAndTimeField(DateTimeField):
    """ I need a way to set the day of the week without caring about the actual day
        Expecting format: <Day of the week> <hour:minutes> <am/pm>
        ex: Wednesday 6 pm
        ex: Wednesday 6:30 pm
    """
    def process_formdata(self, valuelist):
        map = {
          'monday':1,
          'tuesday':2,
          'wednesday':3,
          'thursday':4,
          'friday':5,
          'saturday':6,
          'sunday':7,
        }

        if valuelist:
            # we shouldn't get multiple values, but if we do, join them
            date_str = u' '.join(valuelist)
            valuelist = date_str.split()
            try:
                day = map[valuelist[0].lower()]
                hour_min = valuelist[1].split(':')
                hour = int(hour_min[0])
                if len(hour_min) == 2:
                    minutes = int(hour_min[1])
                else:
                    minutes = 0
                if valuelist[2].lower() == 'pm':
                  hour += 12
                self.data = datetime.datetime(1900, 01, day, hour, minutes)
            except ValueError:
                self.data = None
                raise

class GelGroup_Form(Form):
    Title = TextField(u'Title', validators=[validators.required()])
    DayAndTime = DayAndTimeField(u'Day And Time', validators=[validators.required()], format=u'%A %I %p')
    Leaders = TextField(u'Leaders', validators=[validators.required()])
    ContactEmail = TextField(u'ContactEmail', validators=[validators.required()])
    Description = TextAreaField(u'Description', validators=[validators.required(), validators.length(max=500)])


class GelGroup(BaseModel):
    Createdby = db.UserProperty(auto_current_user_add=True)
    CreationDateTime = UtcDateTimeProperty(auto_now_add=True)

    Title = db.StringProperty(
      verbose_name="Title",
      required=True,
    )
    DayAndTime = db.DateTimeProperty(
      verbose_name="Day And Time",
      required=True,
    )
    Leaders = db.StringProperty(
      verbose_name="Leaders",
      required=True,
    )
    ContactEmail = db.StringProperty(
      verbose_name="Leaders",
      required=True,
    )
    Description = db.TextProperty(
      verbose_name="Description",
      required=True,
    )

    @db.ComputedProperty
    def FormattedDayAndTime(self):
        if self.DayAndTime.minute == 0:
            return self.DayAndTime.strftime('%A') + ' ' + self.DayAndTime.strftime('%I').lstrip('0') + self.DayAndTime.strftime('%p').lower()
        else:
            return self.DayAndTime.strftime('%A') + ' ' + self.DayAndTime.strftime('%I').lstrip('0') + ':' + str(self.DayAndTime.minute) + self.DayAndTime.strftime('%p').lower()
