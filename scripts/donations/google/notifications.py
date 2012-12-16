import logging
from google.appengine.ext import webapp
from scripts import BaseHandler
from scripts.donations.google import NotificationHandler
from scripts.gaesettings import gaesettings

class GoogleCheckout_NotificationHandler(NotificationHandler):
    def merchant_details():
        "return a tuple of your merchant details (your_id, your_key)"
        if gaesettings.google_checkout_use_sandbox:
            return (gaesettings.google_checkout_sandbox_merchant_id, gaesettings.google_checkout_sandbox_merchant_key)
        else:
            return (gaesettings.google_checkout_merchant_id, gaesettings.google_checkout_merchant_key)

    def new_order(self):
        # put into database?
        logging.info("got a new order notification", self.notification)


application = webapp.WSGIApplication([
  ('/donations/google/notifications.*', GoogleCheckout_NotificationHandler),
  ], debug=BaseHandler.debug)