import time

from google.appengine.api import logservice
from google.appengine.api.mail import EmailMessage
from google.appengine.ext import webapp
from scripts.main import BaseHandler

class EmailLogs(BaseHandler):
  def get(self):
    errors = []
    end = time.time()
    start = end - (24 * 60 * 60)
    for log in logservice.fetch(start_time=start, end_time=end, include_app_logs=True, minimum_log_level=logservice.LOG_LEVEL_ERROR):
      for app_log in log.app_logs:
        if app_log.level >= 3:
          errors.append(app_log.message.split('\n')[-1])

    self.response.out.write("There are %s errors.<br />" % len(errors))
    for e in errors:
      self.response.out.write(e + "<br />")

    if len(errors) > 0:
      message = EmailMessage()
      message.sender = "Rolla CCF Website Errors <admin@rollaccf.org>"
      message.to = "admin@rollaccf.org"
      message.subject = "CCF Website Errors (%s)" % len(errors)
      message.body = "\n".join(errors)
      message.send()

application = webapp.WSGIApplication([
  ('/tasks/errorReport', EmailLogs),
  ], debug=BaseHandler.debug)
