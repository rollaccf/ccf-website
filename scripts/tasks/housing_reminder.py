import datetime
from google.appengine.api.mail import EmailMessage
from google.appengine.ext import webapp
from scripts.main import BaseHandler
from scripts.database_models.housingapplication import HousingApplication
from scripts.gaesettings import gaesettings

class HousingReminder(BaseHandler):
    def get(self):
        time_delay = datetime.datetime.now() - datetime.timedelta(days=gaesettings.HousingApplication_ReminderEmailDelayDays)
        unacknowledge_apps = HousingApplication.gql("WHERE Acknowledged = False AND TimeSubmitted < :1", time_delay).fetch(50)

        self.response.out.write("There are %s unacknowledged applications.<br />" % len(unacknowledge_apps))
        for app in unacknowledge_apps:
            self.response.out.write(app.FullName + ' <a href="/manage/housing_applications/view/'+str(app.key())+'" >link</a>'  + "<br />")

        if len(unacknowledge_apps) > 0:
            message = EmailMessage()
            message.sender = "Rolla CCF Housing Application Reminder <admin@rollaccf.org>"
            message.to = "admin@rollaccf.org" #[gaesettings.HousingApplicationCch_CompletionEmail, gaesettings.HousingApplicationWcch_CompletionEmail]
            message.subject = "Rolla CCF Housing Application Reminder (%s)" % datetime.datetime.now().strftime('%b-%d-%Y')
            message.html = "<p>Unacknowledged applications:</p>"
            for app in unacknowledge_apps:
                message.html += '<p>{name}<br /><a href="{link}">{link}</a></p>'.format(name=app.FullName, link="www.rollaccf.org/manage/housing_applications/view/"+str(app.key()))
            message.send()

application = webapp.WSGIApplication([
  ('/tasks/housing_reminder', HousingReminder),
  ], debug=BaseHandler.debug)
