import os
import datetime
from google.appengine.api.mail import EmailMessage
from google.appengine.ext import webapp
from . import Tasks_BaseHandler
from scripts.database_models.housing_application import HousingApplication
from scripts.utils.tzinfo import Central


class HousingReminder(Tasks_BaseHandler):
    def generate_html(self, unacknowledged_apps):
        app_link = "{host}/manage/housing_applications/view/{key}".format(host=os.environ['HTTP_HOST'], key="{key}")
        app_html_template = '<p>{name}<br /><a href="{link}">{link}</a></p>'.format(name='{name}', link=app_link)

        message_html = "<p>Unacknowledged applications:</p>"
        for app in unacknowledged_apps:
            message_html += app_html_template.format(name=app.FullName, key=app.key.urlsafe())

        return message_html

    def get(self):
        time_delay = datetime.timedelta(days=self.settings.HousingApplication_ReminderEmailDelayDays)
        time_offset = datetime.datetime.utcnow() - time_delay
        unacknowledged_apps = HousingApplication.query(
            HousingApplication.Stage == 0,
            HousingApplication.TimeSubmitted < time_offset
        ).fetch(20)

        message_html = self.generate_html(unacknowledged_apps)
        self.response.out.write(message_html)

        if len(unacknowledged_apps) > 0:
            message = EmailMessage()
            message.sender = "CCF Housing Application Reminder <housing@rollaccf.org>"
            message.to = [self.settings.HousingApplicationCch_CompletionEmail,
                          self.settings.HousingApplicationWcch_CompletionEmail]
            message.subject = "CCF Housing Application Reminder ({date})".format(
                date=datetime.datetime.now(tz=Central).strftime('%b-%d-%Y'),
            )
            message.html = message_html
            message.send()


application = webapp.WSGIApplication([
    ('/tasks/housing_reminder', HousingReminder),
    ], debug=Tasks_BaseHandler.debug)
