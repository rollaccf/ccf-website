import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from scripts.globals import TEMPLATE_PATH
from django.template.loader import get_template
from django.template.context import Context


class BaseHandler(webapp.RequestHandler):
  def render_template(self, filename, template_args):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    path = os.path.join(TEMPLATE_PATH, filename)
    templ = get_template(path)
    self.response.out.write(templ.render(Context(template_args)))


class MainHandler(BaseHandler):
  def get(self):
    self.render_template("index.html", { 'title':"CCF STUFF", 'headerText':"Welcome to CCF" })


application = webapp.WSGIApplication([('/', MainHandler)], debug=True)

