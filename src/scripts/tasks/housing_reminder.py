import datetime
from google.appengine.api.mail import EmailMessage
from google.appengine.ext import webapp
from . import Tasks_BaseHandler
from scripts.database_models.housingapplication import HousingApplication
from scripts.utils.tzinfo import Central


class HousingReminder(Tasks_BaseHandler):
    def get(self):
        time_delay = datetime.timedelta(days=self.settings.HousingApplication_ReminderEmailDelayDays)
        time_offset = datetime.datetime.utcnow() - time_delay
        unacknowledged_apps = HousingApplication.query(
            HousingApplication.Acknowledged == False,
            HousingApplication.TimeSubmitted < time_offset
        ).fetch(20)

        self.response.out.write("There are %s unacknowledged applications.<br />" % len(unacknowledged_apps))
        text = '{} <a href="/manage/housing_applications/view/{}" >link</a><br />'
        for app in unacknowledged_apps:
            self.response.out.write(text.format(app.FullName, str(app.key.urlsafe())))

        if len(unacknowledged_apps) > 0:
            message = EmailMessage()
            message.sender = "Rolla CCF Housing Application Reminder <admin@rollaccf.org>"
            message.to = [self.settings.HousingApplicationCch_CompletionEmail,
                          self.settings.HousingApplicationWcch_CompletionEmail]
            message.subject = "Rolla CCF Housing Application Reminder (%s)" % datetime.datetime.now(
                tz=Central).strftime('%b-%d-%Y')
            message.html = "<p>Unacknowledged applications:</p>"
            for app in unacknowledged_apps:
                app_html = '<p>{name}<br /><a href="{link}">{link}</a></p>'
                app_link = "www.rollaccf.org/manage/housing_applications/view/{key}".format(key=app.key.urlsafe())
                app_html.format(name=app.FullName, link=app_link)
                message.html += app_html
            message.send()


application = webapp.WSGIApplication([
    ('/tasks/housing_reminder', HousingReminder),
    ], debug=Tasks_BaseHandler.debug)
