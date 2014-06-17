import re
from google.appengine.ext import webapp
from scripts import BaseHandler
from scripts.donations.google import client

from wtforms import validators
from wtforms.form import Form
from wtforms.fields import *


class OnetimeGiftForm(Form):
    Donation_Amount = TextField(u'Donation Amount', validators=[validators.required()])
    #Item_name = HiddenField()

    def validate_Donation_Amount(form, field):
        pattern = "^[0-9]+(\.([0-9]+))?$"
        if not re.match(pattern, field.data):
            raise validators.ValidationError("You must enter a valid donation.")


class SubscriptionGiftForm(Form):
    Donation_Amount = TextField(u'Donation Amount', validators=[validators.required()])
    Times = IntegerField(u'', validators=[validators.required()], default=12)

    def validate_Donation_Amount(form, field):
        pattern = "^[0-9]+(\.([0-9]+))?$"
        if not re.match(pattern, field.data):
            raise validators.ValidationError("You must enter a valid donation.")


class Legacy_BaseHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(Legacy_BaseHandler, self).__init__(*args, **kwargs)


class LegacyHandler(Legacy_BaseHandler):
    def get(self):
        self.render_template("legacy/legacy.html")


class LegacyDonateHandler(Legacy_BaseHandler):
    def get(self):
        self.template_vars['onetime_form'] = OnetimeGiftForm()
        self.template_vars['subscription_form'] = SubscriptionGiftForm()
        self.render_template("legacy/donate.html")


class Onetime_Handler(BaseHandler):
    def post(self):
        form = OnetimeGiftForm(self.request.POST)
        if form.validate():
            unit_price = form.Donation_Amount.data

            items = [{'name': "One Time Donation to Christian Campus Fellowship",
                      'description': "Supporting the CCF Building Fund",
                      'unit_price': unit_price,
                      'quantity': "1",
                     },
            ]
            redirect_url = client.create_new_order(items=items, merchant_private_data="TEST Merchant private data")
            self.redirect(str(redirect_url))
        else:
            # TODO: send errors/data to the get handler
            self.redirect('/legacy/donate')


class Subscription_Handler(BaseHandler):
    def post(self):
        form = SubscriptionGiftForm(self.request.POST)
        if form.validate():
            unit_price = form.Donation_Amount.data
            times = form.Times.data

            subscription = {'name': "{} Month Donation to Christian Campus Fellowship".format(times),
                            'description': "Supporting the CCF Building Fund",
                            'unit_price': unit_price,
                            'times': times,
                            'quantity': "1",
            }
            redirect_url = client.create_new_order(subscription=subscription,
                                                   merchant_private_data="TEST Merchant private data")
            self.redirect(str(redirect_url))
        else:
            # TODO: send errors/data to the get handler
            self.redirect('/legacy/donate')


application = webapp.WSGIApplication([
    ('/legacy/?', LegacyHandler),
    ('/legacy/donate/onetime.*', Onetime_Handler),
    ('/legacy/donate/subscription.*', Subscription_Handler),
    ('/legacy/donate.*', LegacyDonateHandler),
    ], debug=BaseHandler.debug)
